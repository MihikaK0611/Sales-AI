"""
Upload History page for Sales Intelligence AI
View all uploaded files and their processing status
"""
import streamlit as st
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import require_authentication, get_user_id, init_session_state
from database import get_user_files
import pandas as pd

st.set_page_config(
    page_title="Upload History - Sales Intelligence AI",
    page_icon="📁",
    layout="wide"
)

# Initialize session state
init_session_state()

# Require authentication
require_authentication()

# Get current user
user_id = get_user_id()

# Custom CSS
st.markdown("""
    <style>
    /* Clean White Background Theme */
    .main {
        background-color: #ffffff;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }

    /* Headers */
    h1 {
        color: #111827;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    h2, h3 {
        color: #374151;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e5e7eb;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        color: #374151;
    }
    
    .stButton > button:hover {
        background-color: #f9fafb;
        border-color: #d1d5db;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transform: translateY(-1px);
    }
    
    /* Status badges */
    .status-completed {
        background: #dcfce7;
        color: #166534;
        padding: 0.4rem 0.9rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-failed {
        background: #fee2e2;
        color: #991b1b;
        padding: 0.4rem 0.9rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-processing {
        background: #fef3c7;
        color: #92400e;
        padding: 0.4rem 0.9rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        background-color: #ffffff;
        padding: 1rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("📁 Upload History")
st.markdown("View all your uploaded files and their processing status")

# Get user files
if user_id:
    files_df = get_user_files(user_id)
    
    if not files_df.empty:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Files", len(files_df))
        
        with col2:
            completed = len(files_df[files_df['processing_status'] == 'completed'])
            st.metric("Completed", completed)
        
        with col3:
            failed = len(files_df[files_df['processing_status'] == 'failed'])
            st.metric("Failed", failed)
        
        with col4:
            total_records = files_df['records_extracted'].sum()
            st.metric("Total Records", int(total_records))
        
        st.markdown("---")
        
        # Format the dataframe for display
        display_df = files_df.copy()
        
        # Format file size
        display_df['file_size'] = display_df['file_size'].apply(
            lambda x: f"{x/1024:.1f} KB" if x < 1024*1024 else f"{x/(1024*1024):.1f} MB"
        )
        
        # Format dates
        display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
        display_df['updated_at'] = pd.to_datetime(display_df['updated_at']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Rename columns for better display
        display_df = display_df.rename(columns={
            'filename': 'File Name',
            'file_type': 'Type',
            'file_size': 'Size',
            'processing_status': 'Status',
            'records_extracted': 'Records',
            'error_message': 'Error',
            'created_at': 'Uploaded At',
            'updated_at': 'Updated At'
        })
        
        # Select columns to display
        display_columns = ['File Name', 'Type', 'Size', 'Status', 'Records', 'Uploaded At', 'Updated At']
        
        # Add error column if there are any errors
        if display_df['Error'].notna().any():
            display_columns.append('Error')
        
        # Display the dataframe
        st.subheader("📋 File Upload History")
        
        # Add filter by status
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "completed", "failed", "processing"]
        )
        
        if status_filter != "All":
            filtered_df = display_df[display_df['Status'] == status_filter]
        else:
            filtered_df = display_df
        
        # Display filtered data
        st.dataframe(
            filtered_df[display_columns],
            use_container_width=True,
            hide_index=True
        )
        
        # Show detailed information for failed files
        failed_files = display_df[display_df['Status'] == 'failed']
        if not failed_files.empty:
            st.markdown("---")
            st.subheader("⚠️ Failed Uploads")
            st.warning(f"Found {len(failed_files)} failed upload(s). Please review the errors below:")
            
            for idx, row in failed_files.iterrows():
                with st.expander(f"❌ {row['File Name']} - {row['Uploaded At']}"):
                    st.error(f"**Error:** {row['Error']}")
                    st.info("💡 **Tip:** Make sure your file format matches the expected structure. Check the documentation for supported formats.")
        
        # Tips section
        st.markdown("---")
        st.subheader("💡 Tips")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📤 **Supported Formats:** PDF, Excel (.xlsx, .xls), CSV")
            st.info("📊 **Best Practice:** Upload files regularly to keep your analytics up-to-date")
        
        with col2:
            st.info("✅ **Completed:** File processed successfully and data extracted")
            st.info("❌ **Failed:** File processing encountered an error - check the error message")
        
    else:
        st.info("📤 No files uploaded yet. Go to the dashboard to upload your first file!")
        
        if st.button("🏠 Go to Dashboard", type="primary"):
            st.switch_page("app.py")

else:
    st.error("Unable to load user information. Please try logging in again.")

# Made with Bob
