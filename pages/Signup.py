"""
Simple & Clean Signup Page
Matches the Login UI properly
"""

import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import sign_up, init_session_state

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sign Up • SalesAI",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_session_state()

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Hide Streamlit UI */
#MainMenu, footer, header { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
button[aria-label="Open sidebar"] { display: none !important; }

/* Base */
html, body, .stApp {
    margin: 0;
    padding: 0;
    background: #ffffff;
    font-family: 'Inter', sans-serif;
}

div.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    min-height: 100vh;
}

/* Split Layout */
[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    min-height: 100vh;
    align-items: stretch !important;
}

/* Left Column */
[data-testid="stHorizontalBlock"] > div:first-child {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
    padding: 0 !important;
}

[data-testid="stHorizontalBlock"] > div:first-child::before {
    content: '';
    position: absolute;
    top: -20%;
    left: -20%;
    width: 80%;
    height: 80%;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
    pointer-events: none;
}

/* Right Column */
[data-testid="stHorizontalBlock"] > div:last-child {
    background: #ffffff !important;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
}

[data-testid="stHorizontalBlock"] > div:last-child > div:first-child {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 40px !important;
}

[data-testid="stHorizontalBlock"] > div:last-child .stMarkdown,
[data-testid="stHorizontalBlock"] > div:last-child .stTextInput,
[data-testid="stHorizontalBlock"] > div:last-child .stForm,
[data-testid="stHorizontalBlock"] > div:last-child .stButton,
[data-testid="stHorizontalBlock"] > div:last-child .stFormSubmitButton,
[data-testid="stHorizontalBlock"] > div:last-child .stCheckbox,
[data-testid="stHorizontalBlock"] > div:last-child .stAlert {
    width: 100%;
    max-width: 450px;
}

/* Left Panel Content */
.left-panel-inner {
    position: relative;
    z-index: 1;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px 50px;
}

.panel-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 30px;
    width: fit-content;
}

.panel-title {
    font-size: 48px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 20px;
}

.panel-desc {
    font-size: 16px;
    color: rgba(255,255,255,0.85);
    line-height: 1.7;
    margin-bottom: 35px;
    max-width: 500px;
}

.panel-stats {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.stat-pill {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 10px 18px;
    font-size: 14px;
    color: #ffffff;
    font-weight: 500;
}

/* Form Header */
.form-header {
    width: 100%;
    max-width: 450px;
    margin-bottom: 20px;
}

.form-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 40px;
}

.form-logo-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3);
}

.form-logo-text {
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.form-title {
    font-size: 36px;
    font-weight: 800;
    color: #111827;
    line-height: 1.2;
    margin-bottom: 12px;
}

.form-subtitle {
    font-size: 16px;
    color: #6b7280;
    line-height: 1.6;
    margin-bottom: 30px;
}

/* Labels */
.stTextInput label, .stCheckbox label {
    color: #374151 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* Inputs */
.stTextInput input {
    background: #ffffff !important;
    border: 2px solid #e5e7eb !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    color: #111827 !important;
    font-size: 15px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

.stTextInput input:focus {
    border: 2px solid #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
    outline: none !important;
}

.stTextInput input::placeholder {
    color: #9ca3af !important;
}

/* Checkbox */
.stCheckbox {
    margin: 10px 0;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    width: 100% !important;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
}

/* Divider */
.divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 30px 0 25px;
    color: #9ca3af;
    font-size: 13px;
    font-weight: 500;
    width: 100%;
    max-width: 450px;
}

.divider::before, .divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #e5e7eb;
}

/* Footer */
.footer-wrap {
    width: 100%;
    max-width: 450px;
}

.footer-dots {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 6px;
    margin-top: 30px;
}

.footer-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #d1d5db;
    display: inline-block;
}

.footer-dots span.active {
    background: #3b82f6;
    width: 20px;
    border-radius: 3px;
}

.footer-text {
    text-align: center;
    color: #9ca3af;
    font-size: 12px;
    margin-top: 12px;
    font-weight: 500;
}

/* Alerts */
.stAlert {
    border-radius: 12px !important;
    font-size: 14px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# AUTH CHECK
# =========================================================

if st.session_state.authenticated:
    st.success("Already logged in")
    st.switch_page("app.py")

# =========================================================
# SPLIT LAYOUT
# =========================================================

left_col, right_col = st.columns([1, 1], gap="small")

# ── LEFT ────────────────────────────────────────────────
with left_col:
    st.markdown("""
    <div class="left-panel-inner">
        <div class="panel-badge">✨ AI Powered Platform</div>
        <div class="panel-title">Build smarter<br>sales pipelines<br>with AI.</div>
        <div class="panel-desc">
            Create your account to unlock intelligent forecasting,
            real-time analytics, automated reporting,
            and AI-powered sales insights.
        </div>
        <div class="panel-stats">
            <div class="stat-pill">📈 Smart Analytics</div>
            <div class="stat-pill">⚡ Instant Reports</div>
            <div class="stat-pill">🔒 Enterprise Security</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT ───────────────────────────────────────────────
with right_col:
    # Header
    st.markdown("""
    <div class="form-header">
        <div class="form-logo">
            <div class="form-logo-icon">📝</div>
            <div class="form-logo-text">SalesAI</div>
        </div>
        <div class="form-title">Create Account</div>
        <div class="form-subtitle">
            Join the next generation AI-powered sales platform.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Form
    with st.form("signup_form"):
        full_name = st.text_input(
            "Full Name",
            placeholder="John Doe"
        )

        email = st.text_input(
            "Email Address",
            placeholder="you@example.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password"
        )

        agree = st.checkbox(
            "I agree to the Terms & Privacy Policy"
        )

        submit = st.form_submit_button("🚀 Create Account")

    # Form Logic
    if submit:
        if not full_name or not email or not password or not confirm_password:
            st.error("Please fill all fields")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif not agree:
            st.error("Please accept Terms & Privacy Policy")
        else:
            with st.spinner("Creating account..."):
                success, message, user = sign_up(
                    email,
                    password,
                    full_name
                )

                if success:
                    st.success(message)
                    time.sleep(2)
                    st.switch_page("pages/Login.py")
                else:
                    st.error(message)

    # Divider
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)

    # Login Button
    if st.button("🔐 Login Instead"):
        st.switch_page("pages/Login.py")

    # Footer
    st.markdown("""
    <div class="footer-wrap">
        <div class="footer-dots">
            <span></span><span class="active"></span><span></span>
        </div>
        <div class="footer-text">Secure • Fast • AI Powered</div>
    </div>
    """, unsafe_allow_html=True)

# Made with Bob
