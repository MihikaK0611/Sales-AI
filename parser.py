"""
PDF Parser for Sales Intelligence AI
Parses Tally-exported Sales Register PDFs (Page A sections only).

Format notes:
  - Each (A) page contains one table; Page (B) pages contain running totals only.
  - Transaction header lines look like:
        DD-Mon-YYYY  CUSTOMER NAME  B1            VCH_NO  [narration]  QTY unit
        DD-Mon-YYYY  CUSTOMER NAME  ROUGH ESTIMATE  VCH_NO  narration   QTY unit
  - Product lines look like:
        PROD_CODE  DESCRIPTION  QTY unit  RATE.00/unit
  - Rates are only available in the plain-text extraction, not the table cells.
  - The "Rate" column is absent from pdfplumber's table output; we parse plain text.
"""

import re
import logging
from typing import Optional

import pandas as pd
import pdfplumber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# Transaction header — matches BOTH "B1" and "ROUGH ESTIMATE" voucher types.
# B1 lines have no narration field:
#   22-Jan-2026 BERA COMPLEX B1 21-1-2026 101 pair
# ROUGH ESTIMATE lines have a narration field between vch_no and qty:
#   22-Jan-2026 ASIM SHOE CENTER ROUGH ESTIMATE JAN4-D-065 hira/januka dd 20 pair
_HEADER = re.compile(
    r'^(\d{1,2}-[A-Za-z]{3}-\d{4})\s+'   # group 1 — date
    r'(.+?)\s+'                             # group 2 — customer name (lazy)
    r'(B1|ROUGH ESTIMATE)\s+'              # group 3 — voucher type
    r'(\S+)'                               # group 4 — voucher number
    r'(?:\s+.+?)?\s+'                      # optional narration (non-capturing)
    r'(\d+)\s*(pair|PCS\.?)\s*$'           # group 5/6 — total qty + unit
)

# Product line with rate:  CODE  DESCRIPTION  QTY  unit  RATE.00/unit
_PRODUCT = re.compile(
    r'^(\S+)\s+(.+?)\s+(\d+)\s*(pair|PCS\.?)\s+([\d,]+\.\d+)/(pair|PCS\.?)\s*$'
)

# Product line without rate (rare — e.g. SM-375 BLACK /RED (G.SPORT) 1 pair)
_PRODUCT_NORATE = re.compile(
    r'^(\S+)\s+(.+?)\s+(\d+)\s*(pair|PCS\.?)\s*$'
)

# Lines to ignore completely
_SKIP_LINES = frozenset({
    'Grand Total', 'continued ...', 'Ref.',
    'Date Particulars Voucher Type Vch No. Voucher Narration Quantity Rate',
})

# Page prefixes that are always metadata / header text
_SKIP_PREFIXES = (
    '2025-2026', 'Sales Register', 'For ', 'Page ', 'Printed on', 'Date Particulars',
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_page_b(text: str) -> bool:
    """Return True if this page contains only running totals (Page B section)."""
    return 'Gross Total' in text and 'SALES' in text and 'Page (A)' not in text


def classify_product_category(product_name: str) -> str:
    """Classify a product into a category based on keywords in its name."""
    u = product_name.upper()
    if 'SLIPPER' in u:
        return 'Slipper'
    if 'SANDAL' in u:
        return 'Sandal'
    if 'HALF CLOSE' in u or 'CLOSE' in u:
        return 'Closed Shoes'
    if 'CHAPPAL' in u:
        return 'Chappal'
    if 'SPORT SHOE' in u or ('SHOES' in u and 'SANDAL' not in u):
        return 'Shoes'
    if any(k in u for k in ('SHOE CLEANER', 'CLEANING CREAM', 'WET WIPES', 'POLISH', 'BRUSH')):
        return 'Accessories'
    if 'BOOT' in u:
        return 'Boots'
    if 'HEEL' in u:
        return 'Heels'
    if 'CLOTH' in u:
        return 'Casual Shoes'
    return 'Other'


def _clean_amount(value: str) -> float:
    """Strip commas and return float, or 0.0 on failure."""
    try:
        return float(value.replace(',', ''))
    except (ValueError, AttributeError):
        return 0.0


# ---------------------------------------------------------------------------
# Core parsers
# ---------------------------------------------------------------------------

def parse_sales(file) -> pd.DataFrame:
    """
    Parse a Tally Sales Register PDF and return a normalised DataFrame.

    Captures ALL voucher types (B1, ROUGH ESTIMATE) and every customer.

    Returns columns:
        invoice_date, invoice_number, customer_name, customer_contact,
        product_name, category, quantity, unit_price, revenue, payment_terms
    """
    rows = []
    current_date: Optional[str] = None
    current_customer: Optional[str] = None
    current_voucher_type: Optional[str] = None
    current_voucher_no: Optional[str] = None

    try:
        with pdfplumber.open(file) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if not text:
                    continue

                # Page (B) pages only carry running totals — skip entirely.
                if _is_page_b(text):
                    logger.debug(f"Page {page_num}: Page (B) — skipped")
                    continue

                # Pull the report date from the page header ("For DD-Mon-YYYY")
                date_match = re.search(r'For\s+(\d{1,2}-[A-Za-z]{3}-\d{4})', text)
                if date_match:
                    current_date = date_match.group(1)

                logger.debug(f"Page {page_num}: processing (date={current_date})")

                for raw_line in text.split('\n'):
                    line = raw_line.strip()

                    # Skip blank, known-static, and metadata lines
                    if not line or line in _SKIP_LINES:
                        continue
                    if any(line.startswith(p) for p in _SKIP_PREFIXES):
                        continue

                    # ── Transaction header ──────────────────────────────────
                    m = _HEADER.match(line)
                    if m:
                        current_date = m.group(1)
                        current_customer = m.group(2).strip()
                        current_voucher_type = m.group(3).strip()
                        current_voucher_no = m.group(4).strip()
                        logger.debug(
                            f"  Transaction: {current_customer!r} | "
                            f"{current_voucher_type} | {current_voucher_no}"
                        )
                        continue

                    # ── Product line with rate ──────────────────────────────
                    m = _PRODUCT.match(line)
                    if m and current_customer:
                        product_name = f"{m.group(1)} {m.group(2)}".strip()
                        qty = float(m.group(3))
                        unit_price = _clean_amount(m.group(5))
                        rows.append({
                            'invoice_date':    current_date,
                            'invoice_number':  current_voucher_no,
                            'customer_name':   current_customer,
                            'customer_contact': '',
                            'product_name':    product_name,
                            'category':        classify_product_category(product_name),
                            'quantity':        qty,
                            'unit_price':      unit_price,
                            'revenue':         qty * unit_price,
                            'payment_terms':   current_voucher_type,
                        })
                        continue

                    # ── Product line without rate (edge case) ───────────────
                    m = _PRODUCT_NORATE.match(line)
                    if m and current_customer:
                        product_name = f"{m.group(1)} {m.group(2)}".strip()
                        qty = float(m.group(3))
                        rows.append({
                            'invoice_date':    current_date,
                            'invoice_number':  current_voucher_no,
                            'customer_name':   current_customer,
                            'customer_contact': '',
                            'product_name':    product_name,
                            'category':        classify_product_category(product_name),
                            'quantity':        qty,
                            'unit_price':      0.0,
                            'revenue':         0.0,
                            'payment_terms':   current_voucher_type,
                        })

    except Exception as exc:
        logger.error(f"Error parsing PDF: {exc}", exc_info=True)
        return pd.DataFrame()

    if not rows:
        logger.warning("No data extracted from PDF")
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # Parse dates and drop unresolvable rows
    df['invoice_date'] = pd.to_datetime(
        df['invoice_date'], format='%d-%b-%Y', errors='coerce'
    )
    df = df.dropna(subset=['invoice_date'])

    # Log summary
    logger.info(
        f"Extracted {len(df)} records | "
        f"{df['customer_name'].nunique()} customers | "
        f"Voucher types: {sorted(df['payment_terms'].unique())} | "
        f"Revenue: ₹{df['revenue'].sum():,.2f}"
    )
    logger.info(f"Category breakdown: {df['category'].value_counts().to_dict()}")

    return df


def extract_text(file) -> str:
    """Extract all plain text from a PDF (utility — used by other modules)."""
    text = ''
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
    except Exception as exc:
        logger.error(f"Error extracting text: {exc}")
    return text


def parse_excel(file) -> pd.DataFrame:
    """
    Parse sales data from an Excel file.

    Accepts common column-name variants and normalises to the standard schema.
    """
    try:
        df = pd.read_excel(file)

        column_mapping = {
            # date
            'date': 'invoice_date', 'Date': 'invoice_date', 'Invoice Date': 'invoice_date',
            # customer
            'customer': 'customer_name', 'Customer': 'customer_name',
            'Customer Name': 'customer_name',
            # product
            'product': 'product_name', 'Product': 'product_name',
            'Product Name': 'product_name',
            # quantity
            'qty': 'quantity', 'Qty': 'quantity', 'Quantity': 'quantity',
            # price
            'price': 'unit_price', 'Price': 'unit_price', 'Unit Price': 'unit_price',
            # revenue
            'amount': 'revenue', 'Amount': 'revenue', 'Revenue': 'revenue',
            'Total': 'revenue',
        }
        df = df.rename(columns=column_mapping)

        required = ['invoice_date', 'product_name', 'quantity', 'unit_price']
        if not all(c in df.columns for c in required):
            logger.error(f"Missing required columns. Found: {df.columns.tolist()}")
            return pd.DataFrame()

        if 'revenue' not in df.columns:
            df['revenue'] = df['quantity'] * df['unit_price']
        if 'customer_name' not in df.columns:
            df['customer_name'] = 'Unknown'
        if 'category' not in df.columns:
            df['category'] = df['product_name'].apply(classify_product_category)
        if 'payment_terms' not in df.columns:
            df['payment_terms'] = ''
        if 'customer_contact' not in df.columns:
            df['customer_contact'] = ''

        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df = df.dropna(subset=['invoice_date'])

        logger.info(f"Parsed {len(df)} records from Excel")
        return df

    except Exception as exc:
        logger.error(f"Error parsing Excel: {exc}")
        return pd.DataFrame()


def parse_csv(file) -> pd.DataFrame:
    """
    Parse sales data from a CSV file.

    Reads the CSV then delegates to parse_excel's normalisation logic.
    """
    try:
        df = pd.read_csv(file)

        column_mapping = {
            'date': 'invoice_date', 'Date': 'invoice_date', 'Invoice Date': 'invoice_date',
            'customer': 'customer_name', 'Customer': 'customer_name',
            'Customer Name': 'customer_name',
            'product': 'product_name', 'Product': 'product_name',
            'Product Name': 'product_name',
            'qty': 'quantity', 'Qty': 'quantity', 'Quantity': 'quantity',
            'price': 'unit_price', 'Price': 'unit_price', 'Unit Price': 'unit_price',
            'amount': 'revenue', 'Amount': 'revenue', 'Revenue': 'revenue',
            'Total': 'revenue',
        }
        df = df.rename(columns=column_mapping)

        required = ['invoice_date', 'product_name', 'quantity', 'unit_price']
        if not all(c in df.columns for c in required):
            logger.error(f"Missing required columns. Found: {df.columns.tolist()}")
            return pd.DataFrame()

        if 'revenue' not in df.columns:
            df['revenue'] = df['quantity'] * df['unit_price']
        if 'customer_name' not in df.columns:
            df['customer_name'] = 'Unknown'
        if 'category' not in df.columns:
            df['category'] = df['product_name'].apply(classify_product_category)
        if 'payment_terms' not in df.columns:
            df['payment_terms'] = ''
        if 'customer_contact' not in df.columns:
            df['customer_contact'] = ''

        df['invoice_date'] = pd.to_datetime(df['invoice_date'], errors='coerce')
        df = df.dropna(subset=['invoice_date'])

        logger.info(f"Parsed {len(df)} records from CSV")
        return df

    except Exception as exc:
        logger.error(f"Error parsing CSV: {exc}")
        return pd.DataFrame()