"""
Configuration module for Sales Intelligence AI
Handles both local .env and Streamlit Cloud secrets
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load local .env for development
load_dotenv()

# =========================
# SECRET HELPER
# =========================

def get_secret(key, default=None):
    """
    Priority:
    1. Streamlit Cloud secrets
    2. Local .env
    3. Default value
    """

    # Try Streamlit secrets
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    # Fallback to .env
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
# APPLICATION
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
        if value is None or value == ""
    ]

    if missing:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing)}"
        )

# Validate immediately
validate_config()

# =========================
# DEBUG LOGS
# =========================

print("========== CONFIG DEBUG ==========")
print("SUPABASE_URL:", bool(SUPABASE_URL))
print("SUPABASE_KEY:", bool(SUPABASE_KEY))
print("DB_URL:", bool(DB_URL))
print("ENVIRONMENT:", ENVIRONMENT)
print("==================================")
