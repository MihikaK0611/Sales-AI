"""
User Profile page for Sales Intelligence AI - Improved UI/UX
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import (
    require_authentication,
    get_current_user,
    get_user_email,
    get_user_metadata,
    update_password,
    sign_out,
    init_session_state,
    get_user_id
)
from database import get_user_statistics

st.set_page_config(
    page_title="Profile - Sales Intelligence AI",
    page_icon="👤",
    layout="wide"
)

init_session_state()
require_authentication()

user = get_current_user()
email = get_user_email()
metadata = get_user_metadata()
user_id = get_user_id()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main { background-color: #f4f6fb; }

    .block-container {
        padding: 2.5rem 3rem 3rem 3rem;
        max-width: 1200px;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Profile Header ── */
    .profile-hero {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 60%, #60a5fa 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem 2rem 2rem;
        display: flex;
        align-items: center;
        gap: 1.75rem;
        margin-bottom: 2rem;
        box-shadow: 0 6px 30px rgba(37,99,235,0.25);
        position: relative;
        overflow: hidden;
    }

    .profile-hero::before {
        content: '';
        position: absolute;
        top: -40px; right: -40px;
        width: 220px; height: 220px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
        pointer-events: none;
    }

    .profile-hero::after {
        content: '';
        position: absolute;
        bottom: -60px; left: 30%;
        width: 300px; height: 300px;
        border-radius: 50%;
        background: rgba(255,255,255,0.04);
        pointer-events: none;
    }

    .avatar {
        width: 80px; height: 80px;
        border-radius: 50%;
        background: rgba(255,255,255,0.18);
        border: 3px solid rgba(255,255,255,0.4);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.9rem; font-weight: 700; color: white;
        flex-shrink: 0;
        letter-spacing: -0.5px;
    }

    .hero-text { color: white; }
    .hero-name { font-size: 1.7rem; font-weight: 700; line-height: 1.2; margin-bottom: 0.25rem; }
    .hero-email { font-size: 0.95rem; opacity: 0.85; font-weight: 400; }
    .hero-badge {
        display: inline-block;
        margin-top: 0.6rem;
        background: rgba(255,255,255,0.18);
        border: 1px solid rgba(255,255,255,0.3);
        color: white;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 3px 12px;
        border-radius: 20px;
        letter-spacing: 0.4px;
    }

    /* ── Stat Cards ── */
    .stats-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .stat-card {
        background: white;
        border-radius: 16px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        border: 1.5px solid #e9edf5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
    }

    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(37,99,235,0.12);
        border-color: #93c5fd;
    }

    .stat-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }

    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1d4ed8;
        line-height: 1.1;
        margin-bottom: 0.3rem;
        word-break: break-all;
    }

    .stat-value.small { font-size: 1.1rem; padding-top: 0.35rem; }

    .stat-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    /* ── Section Card ── */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        border: 1.5px solid #e9edf5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1.25rem;
    }

    .section-title {
        font-size: 1rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1.25rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #dbeafe;
        display: flex; align-items: center; gap: 0.5rem;
    }

    /* ── Info rows ── */
    .info-row { margin-bottom: 1rem; }

    .info-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin-bottom: 0.3rem;
    }

    .info-value {
        font-family: 'DM Mono', monospace;
        font-size: 0.875rem;
        background: #f4f6fb;
        border: 1.5px solid #e9edf5;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        color: #374151;
        word-break: break-all;
    }

    /* ── Action Buttons ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        padding: 0.6rem 1rem !important;
        border: 1.5px solid #e5e7eb !important;
        background: white !important;
        color: #374151 !important;
        width: 100%;
        transition: all 0.2s !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        border-color: #3b82f6 !important;
        background: #eff6ff !important;
        color: #1d4ed8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 10px rgba(59,130,246,0.15) !important;
    }

    /* Logout button — danger style via container class trick */
    div[data-testid="stVerticalBlock"] .logout-btn > button {
        border-color: #fecaca !important;
        color: #dc2626 !important;
        background: #fff5f5 !important;
    }

    div[data-testid="stVerticalBlock"] .logout-btn > button:hover {
        background: #fee2e2 !important;
        border-color: #f87171 !important;
        color: #b91c1c !important;
    }

    /* ── Password Form ── */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1.5px solid #e5e7eb !important;
        padding: 12px 14px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.9rem !important;
        background: #fafbff !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
        background: white !important;
    }

    .stTextInput label {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        color: #374151 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ── Password submit ── */
    .stFormSubmitButton > button {
        font-family: 'DM Sans', sans-serif !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 13px 20px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        width: 100%;
        box-shadow: 0 3px 12px rgba(37,99,235,0.3) !important;
        transition: all 0.2s !important;
    }

    .stFormSubmitButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 5px 18px rgba(37,99,235,0.4) !important;
    }

    /* ── Requirements box ── */
    .req-box {
        background: #f0f9ff;
        border: 1.5px solid #bae6fd;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        font-size: 0.83rem;
        color: #0369a1;
    }

    .req-box strong { display: block; margin-bottom: 0.5rem; font-size: 0.85rem; }

    .req-box ul {
        margin: 0;
        padding-left: 1.3rem;
    }

    .req-box li { margin: 0.25rem 0; line-height: 1.5; }

    /* ── Tips ── */
    .tip-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.85rem 1rem;
        background: #f8faff;
        border: 1.5px solid #e0eaff;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        font-size: 0.875rem;
        color: #374151;
        line-height: 1.5;
    }

    .tip-item:last-child { margin-bottom: 0; }
    .tip-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }

    /* ── Alerts ── */
    .stAlert { border-radius: 12px !important; }

    /* ── Divider ── */
    hr { border-color: #e9edf5; margin: 0.5rem 0 1.25rem 0; }
    </style>
""", unsafe_allow_html=True)


# ── Helper ──────────────────────────────────────────────
def info_row(label, value):
    st.markdown(f"""
        <div class="info-row">
            <div class="info-label">{label}</div>
            <div class="info-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


# ── Profile Hero ─────────────────────────────────────────
full_name = (metadata.get('full_name', 'User') if metadata else 'User')
initials = "".join([w[0].upper() for w in full_name.split()[:2]]) if full_name != 'User' else "U"
verified = getattr(user, 'email_confirmed_at', None)
badge_text = "✓ Verified Account" if verified else "⚠ Unverified"

st.markdown(f"""
    <div class="profile-hero">
        <div class="avatar">{initials}</div>
        <div class="hero-text">
            <div class="hero-name">{full_name}</div>
            <div class="hero-email">{email}</div>
            <span class="hero-badge">{badge_text}</span>
        </div>
    </div>
""", unsafe_allow_html=True)


# ── Stats Row ────────────────────────────────────────────
if user_id:
    stats = get_user_statistics(user_id)
    revenue = stats.get('total_revenue', 0)

    # Format revenue compactly to avoid overflow
    if revenue >= 1_000_000:
        rev_display = f"₹{revenue/1_000_000:.2f}M"
    elif revenue >= 100_000:
        rev_display = f"₹{revenue/100_000:.1f}L"
    else:
        rev_display = f"₹{revenue:,.0f}"

    status_icon = "✅" if verified else "⚠️"
    status_text = "Verified" if verified else "Pending"

    st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-icon">📁</div>
                <div class="stat-value">{stats['files_uploaded']}</div>
                <div class="stat-label">Files Uploaded</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📋</div>
                <div class="stat-value">{stats['records_processed']}</div>
                <div class="stat-label">Records Processed</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-value">{rev_display}</div>
                <div class="stat-label">Total Revenue</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">{status_icon}</div>
                <div class="stat-value small">{status_text}</div>
                <div class="stat-label">Account Status</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ── Main Two-Column Layout ───────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

# ── LEFT COLUMN ──────────────────────────────────────────
with col1:

    # Account Information
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Account Information</div>', unsafe_allow_html=True)
    info_row("Email Address", email or "—")
    if metadata and 'full_name' in metadata:
        info_row("Full Name", metadata['full_name'])
    if user_id:
        info_row("User ID", user_id)
    st.markdown('</div>', unsafe_allow_html=True)

    # Quick Actions
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Quick Actions</div>', unsafe_allow_html=True)

    qa_col1, qa_col2 = st.columns(2)
    with qa_col1:
        if st.button("🏠 Dashboard", use_container_width=True):
            st.switch_page("app.py")
    with qa_col2:
        if st.button("📁 Upload History", use_container_width=True):
            st.switch_page("pages/Upload_History.py")

    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
        success, message = sign_out()
        if success:
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.user_id = None
            st.success(f"✅ {message}")
            st.rerun()
        else:
            st.error(f"❌ {message}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Pro Tips
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💡 Pro Tips</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="tip-item">
            <span class="tip-icon">📤</span>
            <span>Upload more sales data to get better insights and trend predictions.</span>
        </div>
        <div class="tip-item">
            <span class="tip-icon">📊</span>
            <span>Check your dashboard regularly to spot new trends and patterns early.</span>
        </div>
        <div class="tip-item">
            <span class="tip-icon">📥</span>
            <span>Export reports from the dashboard to share insights with your team.</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── RIGHT COLUMN ─────────────────────────────────────────
with col2:

    # Change Password
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔒 Change Password</div>', unsafe_allow_html=True)

    with st.form("change_password_form"):
        new_password = st.text_input(
            "New Password",
            type="password",
            placeholder="Enter new password"
        )
        confirm_new_password = st.text_input(
            "Confirm New Password",
            type="password",
            placeholder="Re-enter new password"
        )

        st.markdown("""
            <div class="req-box">
                <strong>🔐 Password Requirements</strong>
                <ul>
                    <li>At least 8 characters long</li>
                    <li>One uppercase letter (A–Z)</li>
                    <li>One lowercase letter (a–z)</li>
                    <li>One number (0–9)</li>
                    <li>One special character (!@#$%^&*)</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

        submit_password = st.form_submit_button("🔄 Update Password", use_container_width=True)

        if submit_password:
            if not new_password or not confirm_new_password:
                st.error("⚠️ Please fill in all fields.")
            elif new_password != confirm_new_password:
                st.error("⚠️ Passwords do not match.")
            else:
                with st.spinner("Updating password…"):
                    success, message = update_password(new_password)
                    if success:
                        st.success(f"✅ {message}")
                    else:
                        st.error(f"❌ {message}")

    st.markdown('</div>', unsafe_allow_html=True)