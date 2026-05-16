"""
Configuration module for Sales Intelligence AI
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env for development
load_dotenv()

def get_secret(key, default=None):
    """
    Read from Streamlit secrets first,
    then fallback to environment variables
    """
    try:
        return st.secrets[key]
    except:
        return os.getenv(key, default)

# =========================
# SUPABASE
# =========================

SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = get_secret("SUPABASE_SERVICE_KEY")

# =========================
# DATABASE
# =========================

DB_URL = get_secret("DB_URL")

# =========================
# APP
# =========================

APP_SECRET_KEY = get_secret(
    "APP_SECRET_KEY",
    "default-secret-key"
)

ENVIRONMENT = get_secret(
    "ENVIRONMENT",
    "development"
)

# =========================
# EMAIL
# =========================

SMTP_HOST = get_secret(
    "SMTP_HOST",
    "smtp.gmail.com"
)

SMTP_PORT = int(
    get_secret("SMTP_PORT", 587)
)

SMTP_USER = get_secret("SMTP_USER")
SMTP_PASSWORD = get_secret("SMTP_PASSWORD")

# =========================
# OCR
# =========================

TESSERACT_PATH = get_secret(
    "TESSERACT_PATH",
    "tesseract"
)

# =========================
# FILES
# =========================

MAX_FILE_SIZE_MB = int(
    get_secret("MAX_FILE_SIZE_MB", 50)
)

ALLOWED_EXTENSIONS = get_secret(
    "ALLOWED_EXTENSIONS",
    "pdf,xlsx,xls,csv,jpg,jpeg,png"
).split(",")

# =========================
# VALIDATION
# =========================

def validate_config():

    required = {
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_KEY": SUPABASE_KEY,
        "DB_URL": DB_URL
    }

    missing = [
        key for key, value in required.items()
        if not value
    ]

    if missing:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing)}"
        )

validate_config()
