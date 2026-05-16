"""
Authentication module using Supabase Auth
Handles user registration, login, password reset, and session management
"""
from typing import Optional, Dict, Any, Tuple
import streamlit as st
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
import re

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def is_valid_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_strong_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, ""


def sign_up(email: str, password: str, full_name: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Register a new user
    
    Args:
        email: User's email address
        password: User's password
        full_name: User's full name
        
    Returns:
        Tuple of (success, message, user_data)
    """
    try:
        # Validate email
        if not is_valid_email(email):
            return False, "Invalid email format", None
        
        # Validate password
        is_valid, error_msg = is_strong_password(password)
        if not is_valid:
            return False, error_msg, None
        
        # Create user account
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name
                }
            }
        })
        
        if response.user:
            return True, "Account created successfully! Please check your email to verify your account.", response.user
        else:
            return False, "Failed to create account. Please try again.", None
            
    except Exception as e:
        error_message = str(e)
        if "already registered" in error_message.lower():
            return False, "This email is already registered. Please login instead.", None
        return False, f"Registration failed: {error_message}", None


def sign_in(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Sign in an existing user
    
    Args:
        email: User's email address
        password: User's password
        
    Returns:
        Tuple of (success, message, session_data)
    """
    try:
        # Validate email
        if not is_valid_email(email):
            return False, "Invalid email format", None
        
        # Sign in user
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.session:
            return True, "Login successful!", response.session
        else:
            return False, "Invalid credentials", None
            
    except Exception as e:
        error_message = str(e)
        if "invalid" in error_message.lower():
            return False, "Invalid email or password", None
        return False, f"Login failed: {error_message}", None


def sign_out() -> Tuple[bool, str]:
    """
    Sign out the current user
    
    Returns:
        Tuple of (success, message)
    """
    try:
        supabase.auth.sign_out()
        return True, "Logged out successfully"
    except Exception as e:
        return False, f"Logout failed: {str(e)}"


def reset_password(email: str) -> Tuple[bool, str]:
    """
    Send password reset email
    
    Args:
        email: User's email address
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Validate email
        if not is_valid_email(email):
            return False, "Invalid email format"
        
        # Send reset email
        supabase.auth.reset_password_for_email(email)
        return True, "Password reset email sent! Please check your inbox."
        
    except Exception as e:
        return False, f"Failed to send reset email: {str(e)}"


def update_password(new_password: str) -> Tuple[bool, str]:
    """
    Update user's password
    
    Args:
        new_password: New password
        
    Returns:
        Tuple of (success, message)
    """
    try:
        # Validate password
        is_valid, error_msg = is_strong_password(new_password)
        if not is_valid:
            return False, error_msg
        
        # Update password
        supabase.auth.update_user({
            "password": new_password
        })
        return True, "Password updated successfully"
        
    except Exception as e:
        return False, f"Failed to update password: {str(e)}"


def get_current_user() -> Optional[Dict[str, Any]]:
    """
    Get current authenticated user
    
    Returns:
        User data if authenticated, None otherwise
    """
    try:
        user = supabase.auth.get_user()
        return user.user if user else None
    except:
        return None


def get_user_id() -> Optional[str]:
    """
    Get current user's ID
    
    Returns:
        User ID if authenticated, None otherwise
    """
    user = get_current_user()
    return user.id if user else None


def get_user_email() -> Optional[str]:
    """
    Get current user's email
    
    Returns:
        User email if authenticated, None otherwise
    """
    user = get_current_user()
    return user.email if user else None


def get_user_metadata() -> Optional[Dict[str, Any]]:
    """
    Get current user's metadata
    
    Returns:
        User metadata if authenticated, None otherwise
    """
    user = get_current_user()
    return user.user_metadata if user else None


def is_authenticated() -> bool:
    """
    Check if user is authenticated
    
    Returns:
        True if user is authenticated, False otherwise
    """
    return get_current_user() is not None


def init_session_state():
    """Initialize session state for authentication"""
    # Check if user is authenticated with Supabase
    try:
        user = supabase.auth.get_user()
        if user and user.user:
            # User is authenticated with Supabase, update session state
            st.session_state.authenticated = True
            st.session_state.user = user.user
            st.session_state.user_id = user.user.id
        else:
            # No active Supabase session
            if 'authenticated' not in st.session_state:
                st.session_state.authenticated = False
            if 'user' not in st.session_state:
                st.session_state.user = None
            if 'user_id' not in st.session_state:
                st.session_state.user_id = None
    except:
        # Error checking session, initialize as not authenticated
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None


def require_authentication():
    """
    Decorator/function to require authentication
    Redirects to login page if not authenticated
    """
    init_session_state()
    
    # Double-check with Supabase session
    try:
        user = supabase.auth.get_user()
        if user and user.user:
            st.session_state.authenticated = True
            st.session_state.user = user.user
            st.session_state.user_id = user.user.id
            return  # User is authenticated
    except:
        pass
    
    if not st.session_state.authenticated:
        st.warning("Please login to access this page")
        st.stop()

# Made with Bob
