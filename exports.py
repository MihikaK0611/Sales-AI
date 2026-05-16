"""
Export functionality for Sales Intelligence AI
Supports Excel and CSV exports
"""
import pandas as pd
from io import BytesIO
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_to_excel(df: pd.DataFrame, filename: str = None) -> BytesIO:
    """
    Export dataframe to Excel file
    
    Args:
        df: DataFrame to export
        filename: Optional filename (not used for BytesIO)
        
    Returns:
        BytesIO object containing Excel file
    """
    try:
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sales Data')
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Sales Data']
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        output.seek(0)
        logger.info(f"Successfully exported {len(df)} records to Excel")
        return output
        
    except Exception as e:
        logger.error(f"Error exporting to Excel: {str(e)}")
        return BytesIO()


def export_to_csv(df: pd.DataFrame) -> str:
    """
    Export dataframe to CSV string
    
    Args:
        df: DataFrame to export
        
    Returns:
        CSV string
    """
    try:
        csv_string = df.to_csv(index=False)
        logger.info(f"Successfully exported {len(df)} records to CSV")
        return csv_string
        
    except Exception as e:
        logger.error(f"Error exporting to CSV: {str(e)}")
        return ""


def create_summary_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a summary report from sales data
    
    Args:
        df: Sales dataframe
        
    Returns:
        Summary dataframe
    """
    if df.empty:
        return pd.DataFrame()
    
    try:
        summary = pd.DataFrame({
            'Metric': [
                'Total Revenue',
                'Total Transactions',
                'Average Transaction Value',
                'Total Quantity Sold',
                'Unique Products',
                'Unique Customers',
                'Date Range'
            ],
            'Value': [
                f"₹{df['revenue'].sum():,.2f}",
                len(df),
                f"₹{df['revenue'].mean():,.2f}",
                int(df['quantity'].sum()),
                df['product_name'].nunique(),
                df['customer_name'].nunique() if 'customer_name' in df.columns else 'N/A',
                f"{df['invoice_date'].min().strftime('%Y-%m-%d')} to {df['invoice_date'].max().strftime('%Y-%m-%d')}"
            ]
        })
        
        return summary
        
    except Exception as e:
        logger.error(f"Error creating summary report: {str(e)}")
        return pd.DataFrame()


def export_analytics_report(df: pd.DataFrame) -> BytesIO:
    """
    Export comprehensive analytics report to Excel with multiple sheets
    
    Args:
        df: Sales dataframe
        
    Returns:
        BytesIO object containing Excel file with multiple sheets
    """
    try:
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Summary sheet
            summary = create_summary_report(df)
            summary.to_excel(writer, index=False, sheet_name='Summary')
            
            # Raw data sheet
            df.to_excel(writer, index=False, sheet_name='Raw Data')
            
            # Top products sheet
            if not df.empty:
                top_products = (
                    df.groupby('product_name')
                    .agg({
                        'quantity': 'sum',
                        'revenue': 'sum'
                    })
                    .reset_index()
                    .sort_values('revenue', ascending=False)
                    .head(20)
                )
                top_products.columns = ['Product', 'Total Quantity', 'Total Revenue']
                top_products.to_excel(writer, index=False, sheet_name='Top Products')
            
            # Customer analysis sheet (if customer data exists)
            if 'customer_name' in df.columns and df['customer_name'].notna().any():
                customer_analysis = (
                    df[df['customer_name'].notna()]
                    .groupby('customer_name')
                    .agg({
                        'revenue': 'sum',
                        'invoice_date': 'count'
                    })
                    .reset_index()
                    .sort_values('revenue', ascending=False)
                    .head(20)
                )
                customer_analysis.columns = ['Customer', 'Total Revenue', 'Number of Transactions']
                customer_analysis.to_excel(writer, index=False, sheet_name='Top Customers')
            
            # Monthly trends sheet
            if not df.empty:
                monthly = (
                    df.groupby(df['invoice_date'].dt.to_period('M'))
                    .agg({
                        'revenue': 'sum',
                        'quantity': 'sum'
                    })
                    .reset_index()
                )
                monthly['invoice_date'] = monthly['invoice_date'].astype(str)
                monthly.columns = ['Month', 'Revenue', 'Quantity']
                monthly.to_excel(writer, index=False, sheet_name='Monthly Trends')
        
        output.seek(0)
        logger.info("Successfully created analytics report")
        return output
        
    except Exception as e:
        logger.error(f"Error creating analytics report: {str(e)}")
        return BytesIO()

# Made with Bob
