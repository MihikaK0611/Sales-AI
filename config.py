"""
Configuration module for Sales Intelligence AI
Loads sensitive credentials from environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Database Configuration
DB_URL = os.getenv("DB_URL")

# Application Configuration
APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "default-secret-key-change-in-production")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# OCR Configuration
TESSERACT_PATH = os.getenv("TESSERACT_PATH", "tesseract")

# File Upload Configuration
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS", "pdf,xlsx,xls,csv,jpg,jpeg,png").split(",")

# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set"""
    required_vars = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "DB_URL": DB_URL
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please create a .env file based on .env.example"
        )

# Validate configuration on import
if ENVIRONMENT == "production":
    validate_config()

# Made with Bob
