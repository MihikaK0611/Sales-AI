import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import sign_in, init_session_state

st.set_page_config(
    page_title="Login • Sales Intelligence AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_session_state()

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── HIDE ALL STREAMLIT CHROME ─────────────────────────────────── */

#MainMenu, footer, header                 { display: none !important; }
section[data-testid="stSidebar"]          { display: none !important; }
[data-testid="collapsedControl"]          { display: none !important; }
[data-testid="stDecoration"]              { display: none !important; }
[data-testid="stStatusWidget"]            { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
button[aria-label="Open sidebar"]         { display: none !important; }
button[aria-label="open sidebar"]         { display: none !important; }
button[title="Open sidebar"]              { display: none !important; }
.stSidebarToggle                          { display: none !important; }

/* ── ZERO OUT PAGE SHELL ───────────────────────────────────────── */

html, body, .stApp {
    margin: 0;
    padding: 0;
    background: #ffffff !important;
    font-family: 'Inter', sans-serif;
}

div.block-container {
    padding: 0 !important;
    max-width: 100% !important;
    min-height: 100vh;
}

/* ── TOP-LEVEL SPLIT ROW ───────────────────────────────────────── */

[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    min-height: 100vh;
    align-items: stretch !important;
}

/* ── LEFT COLUMN ───────────────────────────────────────────────── */

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
    z-index: 0;
}

[data-testid="stHorizontalBlock"] > div:first-child::after {
    content: '';
    position: absolute;
    bottom: -15%;
    right: -15%;
    width: 70%;
    height: 70%;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,0,0,0.1) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ── RIGHT COLUMN ──────────────────────────────────────────────── */

[data-testid="stHorizontalBlock"] > div:last-child {
    background: #ffffff !important;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
}

[data-testid="stHorizontalBlock"] > div:last-child::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(59,130,246,0.05) 0%, transparent 70%);
    pointer-events: none;
}

/* ── CENTER + CONSTRAIN ALL CONTENT IN RIGHT COL ──────────────── */

/* Streamlit wraps each markdown / widget in a div > div chain.
   We target the direct child of the right column and center it. */

[data-testid="stHorizontalBlock"] > div:last-child > div:first-child {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 40px !important;
    box-sizing: border-box;
}

/* Every Streamlit element inside right col gets max-width */
[data-testid="stHorizontalBlock"] > div:last-child .stMarkdown,
[data-testid="stHorizontalBlock"] > div:last-child .stTextInput,
[data-testid="stHorizontalBlock"] > div:last-child .stForm,
[data-testid="stHorizontalBlock"] > div:last-child .stButton,
[data-testid="stHorizontalBlock"] > div:last-child .stFormSubmitButton,
[data-testid="stHorizontalBlock"] > div:last-child .stAlert,
[data-testid="stHorizontalBlock"] > div:last-child .stSpinner {
    width: 100%;
    max-width: 400px;
}

/* ── LEFT PANEL CONTENT ────────────────────────────────────────── */

.left-panel-inner {
    position: relative;
    z-index: 1;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60px 50px;
    box-sizing: border-box;
}

.panel-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 400px;
    height: 400px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.1);
    box-shadow:
        0 0 0 80px rgba(255,255,255,0.05),
        0 0 0 160px rgba(255,255,255,0.025);
    z-index: 0;
    pointer-events: none;
}

.panel-badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.05em;
    margin-bottom: 30px;
    width: fit-content;
}

.panel-title {
    font-family: 'Inter', sans-serif;
    font-size: 48px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.2;
    margin-bottom: 20px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.1);
}

.panel-desc {
    font-size: 16px;
    color: rgba(255,255,255,0.85);
    line-height: 1.7;
    font-weight: 400;
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

/* ── FORM HEADER (logo + title + subtitle) ─────────────────────── */

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
    font-family: 'Inter', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #111827;
}

.form-title {
    font-family: 'Inter', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #111827;
    line-height: 1.2;
    margin-bottom: 12px;
}

.form-title em {
    font-style: normal;
    color: #3b82f6;
}

.form-subtitle {
    font-size: 16px;
    color: #6b7280;
    font-weight: 400;
    line-height: 1.6;
    margin-bottom: 30px;
}

/* ── LABELS ─────────────────────────────────────────────────────── */

.stTextInput label {
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    margin-bottom: 8px !important;
}

/* ── INPUTS ─────────────────────────────────────────────────────── */

.stTextInput input {
    background: #ffffff !important;
    border: 2px solid #e5e7eb !important;
    color: #111827 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 400 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
}

.stTextInput input::placeholder {
    color: #9ca3af !important;
    font-weight: 400 !important;
}

.stTextInput input:focus {
    border: 2px solid #3b82f6 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
    outline: none !important;
}

/* ── SUBMIT BUTTON ──────────────────────────────────────────────── */

.stFormSubmitButton button {
    width: 100% !important;
    border: none !important;
    padding: 14px 24px !important;
    border-radius: 12px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
    transition: all 0.3s ease !important;
    margin-top: 10px;
    box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
}

.stFormSubmitButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59,130,246,0.4) !important;
}

.stFormSubmitButton button:active {
    transform: translateY(0) !important;
}

/* ── DIVIDER ─────────────────────────────────────────────────────── */

.divider {
    display: flex;
    align-items: center;
    gap: 16px;
    margin: 30px 0 25px;
    color: #9ca3af;
    font-size: 13px;
    font-family: 'Inter', sans-serif;
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

/* ── SECONDARY BUTTONS ───────────────────────────────────────────── */

.btn-row {
    display: flex;
    gap: 12px;
    width: 100%;
    max-width: 450px;
}

.btn-secondary {
    flex: 1;
    background: #ffffff;
    border: 2px solid #e5e7eb;
    color: #374151 !important;
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s ease;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    text-decoration: none !important;
    display: block;
    box-sizing: border-box;
}

.btn-secondary:hover {
    background: #f9fafb;
    border-color: #d1d5db;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    color: #111827 !important;
    text-decoration: none !important;
}

/* ── FOOTER ──────────────────────────────────────────────────────── */

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
    font-family: 'Inter', sans-serif;
    margin-top: 12px;
    font-weight: 500;
}

/* ── ALERTS & SPINNER ────────────────────────────────────────────── */

.stAlert {
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

.stSpinner > div {
    border-top-color: #3b82f6 !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# ALREADY LOGGED IN
# =========================

if st.session_state.authenticated:
    st.success("You are already logged in.")
    st.switch_page("app.py")

# =========================
# SPLIT LAYOUT
# =========================

left_col, right_col = st.columns([1, 1], gap="small")

# ── LEFT ────────────────────────────────────────────────────────────
with left_col:
    st.markdown("""
    <div class="left-panel-inner">
        <div class="panel-ring"></div>
        <div>
            <div class="panel-badge">📊 &nbsp; Sales Intelligence</div>
            <div class="panel-title">Turn data into<br>decisions,<br>instantly.</div>
            <div class="panel-desc">
                AI-powered analytics that surfaces what matters most —
                pipeline trends, rep performance, and revenue signals —
                all in one place.
            </div>
            <div class="panel-stats">
                <div class="stat-pill">📈 Real-time insights</div>
                <div class="stat-pill">🤖 AI forecasting</div>
                <div class="stat-pill">⚡ Instant reports</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT ───────────────────────────────────────────────────────────
with right_col:

    # 1. Header block — fully self-contained, no open divs
    st.markdown("""
    <div class="form-header">
        <div class="form-logo">
            <div class="form-logo-icon">📊</div>
            <div class="form-logo-text">SalesAI</div>
        </div>
        <div class="form-title">Welcome <em>back</em></div>
        <div class="form-subtitle">
            Login to access your AI-powered
            sales analytics dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Form widgets — native Streamlit (no HTML wrapper needed)
    with st.form("login_form"):
        email = st.text_input(
            "Email Address",
            placeholder="you@example.com"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )
        login_btn = st.form_submit_button("🚀  Login")

    if login_btn:
        if not email or not password:
            st.error("Please enter email and password")
        else:
            with st.spinner("Signing in..."):
                success, message, user = sign_in(email, password)
                if success:
                    # Update session state immediately
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.success(message)
                    time.sleep(0.5)
                    st.switch_page("app.py")
                else:
                    st.error(message)

    # 3. Divider — self-contained
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)

    # 4. Buttons — self-contained
    st.markdown("""
    <div class="btn-row">
        <a class="btn-secondary" href="/Signup" target="_self">
            📝&nbsp; Create Account
        </a>
        <a class="btn-secondary" href="/Reset_Password" target="_self">
            🔑&nbsp; Forgot Password
        </a>
    </div>
    """, unsafe_allow_html=True)

    # 5. Footer — self-contained
    st.markdown("""
    <div class="footer-wrap">
        <div class="footer-dots">
            <span></span><span class="active"></span><span></span>
        </div>
        <div class="footer-text">Secure &nbsp;·&nbsp; Fast &nbsp;·&nbsp; AI Powered</div>
    </div>
    """, unsafe_allow_html=True)