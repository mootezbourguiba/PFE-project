"""
Login Page

Dashboard-style glassmorphism aviation login screen for AVIONAV.
"""

import base64
import streamlit as st
from pathlib import Path
from PIL import Image
from utils.auth import login


def _image_to_base64(path: Path, mime: str = "image/jpeg") -> str:
    if not path.exists():
        return ""
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def show():
    """Display the AVIONAV login page."""

    BASE_DIR = Path(__file__).parent.parent
    LOGO = BASE_DIR / "assets" / "images" / "logo-Photoroom.png"
    BANNER = BASE_DIR / "assets" / "images" / "banner.jpg"

    banner_b64 = _image_to_base64(BANNER)
    logo_b64 = _image_to_base64(LOGO, mime="image/png")

    # ------------------------------------------------------------------
    # Global styling
    # ------------------------------------------------------------------
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        [data-testid="stSidebar"] {{
            display: none;
        }}

        [data-testid="stAppViewContainer"] {{
            position: relative;
            isolation: isolate;
            overflow: hidden;
            min-height: 100vh;
        }}

        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            inset: 0;
            background:
                linear-gradient(
                    rgba(0, 0, 0, 0.55),
                    rgba(0, 0, 0, 0.55)
                ),
                url({"" if not banner_b64 else banner_b64});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            z-index: -1;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        [data-testid="stMainBlockContainer"] {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-height: 92vh;
            padding: 0;
            margin: 0;
        }}

        /* Global top-left logo badge */
        .login-global-logo {{
            position: fixed;
            top: 24px;
            left: 30px;
            z-index: 100;
        }}

        .login-global-logo img {{
            width: 110px;
            height: 110px;
            padding: 8px;
            background: #FFFFFF !important;
            border-radius: 50%;
            object-fit: contain;
            box-shadow:
                0 0 20px rgba(0, 229, 255, 0.45),
                0 4px 18px rgba(0, 0, 0, 0.35);
        }}

        /* Vertically center the two-column row */
        div[data-testid="stHorizontalBlock"] {{
            align-items: center !important;
        }}

        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:first-child {{
            padding-left: 60px;
        }}

        /* Right-side login glass card */
        div[data-testid="stColumn"]:has(.login-glass-stack) {{
            background: rgba(15, 23, 42, 0.78);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 20px;
            padding: 70px 46px 62px 46px;
            transform: translateX(-60px);
            box-shadow:
                0 28px 90px rgba(0, 0, 0, 0.50),
                inset 0 1px 0 rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }}

        /* Left-side branding */
        .login-left-subtitle {{
            display: block;
            color: #00E5FF;
            font-size: 1.72rem;
            font-weight: 900;
            line-height: 1.2;
            margin: 0 0 1.2rem 0;
            padding-left: 20px;
            text-shadow: 0 0 10px rgba(0, 229, 255, 0.60);
        }}

        .login-left-description {{
            color: rgba(255, 255, 255, 0.70);
            font-size: 14px;
            line-height: 1.85;
            max-width: 440px;
            margin: 0 0 2.4rem 0;
        }}

        /* Platform highlights */
        .highlights-title {{
            color: rgba(255, 255, 255, 0.90);
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin-bottom: 1rem;
            padding-left: 20px;
        }}

        .highlights-grid {{
            display: flex;
            gap: 12px;
            flex-wrap: nowrap;
            align-items: center;
            padding-left: 20px;
        }}

        .highlight-chip {{
            background: transparent;
            border: 1px solid rgba(0, 229, 255, 0.40);
            border-radius: 10px;
            padding: 12px 16px;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: #FFFFFF;
            font-size: 0.85rem;
            font-weight: 500;
            backdrop-filter: blur(4px);
            transition: all 0.2s ease;
        }}

        .highlight-chip:hover {{
            background: rgba(0, 229, 255, 0.08);
            box-shadow: 0 0 16px rgba(0, 229, 255, 0.15);
        }}

        .highlight-chip svg {{
            width: 20px;
            height: 20px;
            color: #00E5FF;
            display: block;
            flex-shrink: 0;
        }}

        /* Login header */
        .login-card-header {{
            color: #FFFFFF;
            font-size: 1.85rem;
            font-weight: 800;
            text-align: center;
            letter-spacing: -0.3px;
            margin: 0 0 1.8rem 0;
        }}

        /* Inputs */
        div[data-testid="stTextInput"] {{
            margin-bottom: 1.2rem !important;
        }}

        div[data-testid="stTextInput"] input {{
            background-color: rgba(10, 18, 26, 0.70) !important;
            color: #F5FAFE !important;
            border: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 12px !important;
            min-height: 56px !important;
            font-size: 0.98rem !important;
            padding: 1rem 1.1rem !important;
            transition: all 0.2s ease;
        }}

        div[data-testid="stTextInput"] input:hover {{
            border-color: rgba(0, 229, 255, 0.65) !important;
            box-shadow: 0 0 14px rgba(0, 229, 255, 0.20) !important;
        }}

        div[data-testid="stTextInput"] input:focus {{
            border-color: #00E5FF !important;
            background-color: rgba(10, 18, 26, 0.85) !important;
            box-shadow:
                0 0 0 1px #00E5FF,
                0 0 20px rgba(0, 229, 255, 0.55),
                0 0 38px rgba(0, 229, 255, 0.35) !important;
        }}

        div[data-testid="stTextInput"] input::placeholder {{
            color: rgba(255, 255, 255, 0.65) !important;
            opacity: 1 !important;
        }}

        div[data-testid="stTextInput"] label {{
            color: rgba(255, 255, 255, 0.88) !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            margin-bottom: 0.35rem !important;
            letter-spacing: 0.2px;
        }}

        div[data-testid="stTextInput"] button {{
            color: #D7E6F0 !important;
        }}

        /* Checkbox */
        div[data-testid="stCheckbox"] {{
            margin: 0.4rem 0 1.4rem 0 !important;
        }}

        div[data-testid="stCheckbox"] label,
        div[data-testid="stCheckbox"] label p {{
            color: rgba(255, 255, 255, 0.88) !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }}

        /* Button */
        div[data-testid="stButton"] button {{
            min-height: 54px;
            border-radius: 20px;
            font-weight: 700;
            font-size: 1.05rem;
            border: none;
            margin-top: 0.4rem;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        div[data-testid="stButton"] button[kind="primary"] {{
            background: linear-gradient(
                90deg,
                #00D4FF,
                #0090C9
            ) !important;
            color: #FFFFFF !important;
            border: none !important;
            width: 100%;
            box-shadow:
                0 4px 14px rgba(0, 0, 0, 0.35),
                0 0 18px rgba(0, 212, 255, 0.25);
        }}

        div[data-testid="stButton"] button[kind="primary"]:hover {{
            background: linear-gradient(
                90deg,
                #00E1FF,
                #00A0D6
            ) !important;
            box-shadow:
                0 0 24px rgba(0, 212, 255, 0.45),
                0 0 48px rgba(0, 212, 255, 0.20);
            transform: scale(1.02);
        }}

        /* Footer */
        .login-page-footer {{
            position: fixed;
            bottom: 18px;
            left: 0;
            width: 100%;
            text-align: center;
            color: rgba(255, 255, 255, 0.55);
            font-size: 0.72rem;
            z-index: 100;
            pointer-events: none;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------------
    # Global logo
    # ------------------------------------------------------------------
    if logo_b64:
        st.markdown(
            f'<div class="login-global-logo"><img src="{logo_b64}" alt="AVIONAV Logo"></div>',
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------
    # Two-column layout
    # ------------------------------------------------------------------
    col_left, col_right = st.columns([1.2, 1], gap="large")

    # ------------------------------------------------------------------
    # LEFT COLUMN — Subtitle, Description, Highlights
    # ------------------------------------------------------------------
    with col_left:
        st.markdown(
            """
            <div class="login-left-subtitle">Intelligent UAV<br>Health Monitoring</div>
            <div class="login-left-description">
                Real-time telemetry monitoring and AI-driven anomaly detection for UAV
                propulsion systems. Predictive maintenance for brushless DC motor bearing wear.
            </div>
            <div class="highlights-title">Platform Highlights</div>
            <div class="highlights-grid">
                <div class="highlight-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                    Real-time Telemetry
                </div>
                <div class="highlight-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>
                    AI Diagnostics
                </div>
                <div class="highlight-chip">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"></path></svg>
                    Fleet Management
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------
    # RIGHT COLUMN — Login form
    # ------------------------------------------------------------------
    with col_right:
        st.markdown('<div class="login-glass-stack"></div>', unsafe_allow_html=True)

        st.markdown(
            '<div class="login-card-header">Login</div>',
            unsafe_allow_html=True,
        )

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        remember = st.checkbox(
            "Remember me",
            key="login_remember",
        )

        if st.button(
            "Login",
            type="primary",
            key="login_button",
            use_container_width=True,
        ):
            with st.spinner("Authenticating..."):
                if login(username, password):
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Invalid username, password, or disabled account.")

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------
    st.markdown(
        '<div class="login-page-footer">© 2026 AVIONAV · v1.0.0</div>',
        unsafe_allow_html=True,
    )
