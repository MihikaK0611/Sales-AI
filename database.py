"""
Database module for Sales Intelligence AI
Handles all database operations with proper security and error handling
"""
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import pandas as pd
from config import DB_URL
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_engine(DB_URL, poolclass=NullPool, echo=False)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_existing_file_id(user_id: str, filename: str, conn) -> Optional[str]:
    """
    Return the existing file_id for this user+filename, or None if not found.
    Used to detect re-uploads of the same file.
    """
    result = conn.execute(
        text("""
            SELECT id FROM file_metadata
            WHERE user_id = :user_id AND filename = :filename
            ORDER BY created_at DESC
            LIMIT 1
        """),
        {"user_id": user_id, "filename": filename}
    )
    row = result.fetchone()
    return str(row[0]) if row else None


def _delete_sales_data_for_file(file_id: str, conn) -> int:
    """Delete all sales_data rows for a given file_id. Returns rows deleted."""
    result = conn.execute(
        text("DELETE FROM sales_data WHERE file_id = :file_id"),
        {"file_id": file_id}
    )
    return result.rowcount


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def insert_data(df: pd.DataFrame, file_id: str, user_id: str) -> bool:
    """
    Insert sales data into the database.

    If data for this file_id already exists it is deleted first, so
    re-uploading the same file always produces a clean, up-to-date result
    rather than doubling the numbers.

    Args:
        df:       DataFrame containing parsed sales data.
        file_id:  UUID of the uploaded file (from file_metadata).
        user_id:  UUID of the authenticated user.

    Returns:
        True if successful, False otherwise.
    """
    try:
        # Validate required columns before touching the DB
        required_columns = ["invoice_date", "product_name", "quantity", "unit_price", "revenue"]
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            logger.error(f"Missing required columns: {missing}")
            return False

        with engine.connect() as conn:
            # Delete any existing rows for this file_id so re-uploads are clean
            deleted = _delete_sales_data_for_file(file_id, conn)
            if deleted:
                logger.info(f"Cleared {deleted} existing rows for file {file_id} before re-insert")
            conn.commit()

        # Add user_id and file_id to dataframe
        df = df.copy()
        df["user_id"] = user_id
        df["file_id"] = file_id

        df.to_sql("sales_data", engine, if_exists="append", index=False, method="multi")

        logger.info(f"Inserted {len(df)} records for file {file_id}")
        return True

    except Exception as e:
        logger.error(f"Error inserting data: {str(e)}")
        return False


def get_or_replace_file_metadata(
    file_id: str,
    user_id: str,
    filename: str,
    file_type: str,
    file_size: int,
) -> str:
    """
    Idempotent file registration.

    If a file with the same filename already exists for this user:
      - deletes its old sales_data rows
      - deletes the old file_metadata row
    Then inserts a fresh file_metadata row with the new file_id.

    Returns the file_id that should be used for subsequent inserts
    (always the new file_id passed in).
    """
    try:
        with engine.connect() as conn:
            existing_file_id = _get_existing_file_id(user_id, filename, conn)

            if existing_file_id:
                logger.info(
                    f"Re-upload detected for '{filename}' "
                    f"(old file_id={existing_file_id}). Replacing data."
                )
                deleted = _delete_sales_data_for_file(existing_file_id, conn)
                logger.info(f"  Deleted {deleted} old sales rows")

                conn.execute(
                    text("DELETE FROM file_metadata WHERE id = :fid"),
                    {"fid": existing_file_id}
                )

            conn.execute(
                text("""
                    INSERT INTO file_metadata
                        (id, user_id, filename, file_type, file_size, processing_status)
                    VALUES
                        (:file_id, :user_id, :filename, :file_type, :file_size, 'processing')
                """),
                {
                    "file_id": file_id,
                    "user_id": user_id,
                    "filename": filename,
                    "file_type": file_type,
                    "file_size": file_size,
                }
            )
            conn.commit()

        logger.info(f"Registered file metadata for '{filename}' (file_id={file_id})")
        return file_id

    except Exception as e:
        logger.error(f"Error in get_or_replace_file_metadata: {str(e)}")
        raise


def create_file_metadata(
    file_id: str,
    user_id: str,
    filename: str,
    file_type: str,
    file_size: int,
) -> bool:
    """
    Create a file_metadata record, replacing any previous record for the
    same user+filename so re-uploads never accumulate duplicate rows.

    Call get_or_replace_file_metadata() directly if you need the returned
    file_id; this wrapper exists for backward compatibility.
    """
    try:
        get_or_replace_file_metadata(file_id, user_id, filename, file_type, file_size)
        return True
    except Exception:
        return False


def update_file_status(
    file_id: str,
    status: str,
    records_extracted: int = 0,
    error_message: Optional[str] = None,
) -> bool:
    """
    Update the processing status of a file_metadata record.

    Args:
        file_id:           UUID of the file.
        status:            'processing' | 'completed' | 'failed'
        records_extracted: Number of records successfully extracted.
        error_message:     Human-readable error details (if status == 'failed').

    Returns:
        True if successful, False otherwise.
    """
    try:
        with engine.connect() as conn:
            conn.execute(
                text("""
                    UPDATE file_metadata
                    SET processing_status = :status,
                        records_extracted = :records,
                        error_message     = :error,
                        updated_at        = NOW()
                    WHERE id = :file_id
                """),
                {
                    "file_id": file_id,
                    "status":  status,
                    "records": records_extracted,
                    "error":   error_message,
                }
            )
            conn.commit()
        return True

    except Exception as e:
        logger.error(f"Error updating file status: {str(e)}")
        return False


def load_data(user_id: str) -> pd.DataFrame:
    """
    Load all sales data for a user, ordered newest-first.

    Args:
        user_id: UUID of the authenticated user.

    Returns:
        DataFrame with the user's sales records, or an empty DataFrame on error.
    """
    try:
        query = text("""
            SELECT
                id,
                invoice_date,
                customer_name,
                product_name,
                category,
                quantity,
                unit_price,
                discount,
                tax_amount,
                revenue,
                invoice_number,
                payment_terms,
                created_at
            FROM sales_data
            WHERE user_id = :user_id
            ORDER BY invoice_date DESC
        """)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"user_id": user_id})

        logger.info(f"Loaded {len(df)} records for user {user_id}")
        return df

    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


def get_file_metadata(user_id: str) -> pd.DataFrame:
    """
    Return file upload metadata for a user.

    Args:
        user_id: UUID of the authenticated user.

    Returns:
        DataFrame with file metadata rows, or empty DataFrame on error.
    """
    try:
        query = text("""
            SELECT
                id,
                filename,
                file_type,
                file_size,
                upload_date,
                processing_status,
                records_extracted
            FROM file_metadata
            WHERE user_id = :user_id
            ORDER BY upload_date DESC
        """)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"user_id": user_id})
        return df

    except Exception as e:
        logger.error(f"Error loading file metadata: {str(e)}")
        return pd.DataFrame()


def get_user_files(user_id: str) -> pd.DataFrame:
    """
    Return full file upload history for a user (includes error_message).

    Args:
        user_id: UUID of the authenticated user.

    Returns:
        DataFrame with file rows, or empty DataFrame on error.
    """
    try:
        query = text("""
            SELECT
                id,
                filename,
                file_type,
                file_size,
                processing_status,
                records_extracted,
                error_message,
                created_at,
                updated_at
            FROM file_metadata
            WHERE user_id = :user_id
            ORDER BY created_at DESC
        """)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"user_id": user_id})
        return df

    except Exception as e:
        logger.error(f"Error getting user files: {str(e)}")
        return pd.DataFrame()


def get_user_statistics(user_id: str) -> Dict[str, Any]:
    """
    Compute headline statistics for the profile page.

    Counts distinct file_ids (not filenames) so the number reflects the
    current set of files, not historical re-uploads.

    Args:
        user_id: UUID of the authenticated user.

    Returns:
        Dict with keys: files_uploaded, records_processed,
                        total_revenue, last_activity.
    """
    try:
        query = text("""
            SELECT
                COUNT(DISTINCT file_id) AS files_uploaded,
                COUNT(*)               AS records_processed,
                SUM(revenue)           AS total_revenue,
                MAX(invoice_date)      AS last_activity
            FROM sales_data
            WHERE user_id = :user_id
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"user_id": user_id})
            row = result.fetchone()

        return {
            "files_uploaded":    row[0] or 0,
            "records_processed": row[1] or 0,
            "total_revenue":     float(row[2] or 0),
            "last_activity":     row[3],
        }

    except Exception as e:
        logger.error(f"Error getting user statistics: {str(e)}")
        return {
            "files_uploaded":    0,
            "records_processed": 0,
            "total_revenue":     0.0,
            "last_activity":     None,
        }


def delete_file_data(file_id: str, user_id: str) -> bool:
    """
    Permanently delete a file and all its associated sales data.

    Enforces user ownership before deletion.

    Args:
        file_id:  UUID of the file to delete.
        user_id:  UUID of the authenticated user (ownership check).

    Returns:
        True if the file was found and deleted, False otherwise.
    """
    try:
        with engine.connect() as conn:
            # Ownership check
            result = conn.execute(
                text("SELECT id FROM file_metadata WHERE id = :fid AND user_id = :uid"),
                {"fid": file_id, "uid": user_id}
            )
            if not result.fetchone():
                logger.warning(f"File {file_id} not found or not owned by user {user_id}")
                return False

            deleted_sales = _delete_sales_data_for_file(file_id, conn)
            conn.execute(
                text("DELETE FROM file_metadata WHERE id = :fid"),
                {"fid": file_id}
            )
            conn.commit()

        logger.info(f"Deleted file {file_id} and {deleted_sales} sales rows")
        return True

    except Exception as e:
        logger.error(f"Error deleting file data: {str(e)}")
        return False