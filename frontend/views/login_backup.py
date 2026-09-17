"""
Login Page

Premium aviation login screen for AVIONAV.
"""

import streamlit as st
from pathlib import Path
from PIL import Image
from utils.auth import login
from components.theme import COLORS


def show():
    """Display the AVIONAV login page."""
    hide_sidebar = """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0A1621 0%, #0E2B3F 60%, #0A1621 100%);
    }
    </style>
    """
    st.markdown(hide_sidebar, unsafe_allow_html=True)

    BASE_DIR = Path(__file__).parent.parent
    LOGO = BASE_DIR / "assets" / "images" / "avionav_logo.png"

    st.markdown("""
    <style>
    .login-hero {
        color: #FFFFFF;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1rem;
    }
    .login-hero span {
        color: #00C2FF;
    }
    .login-sub {
        color: #B8C7D9;
        font-size: 1.05rem;
        line-height: 1.6;
        max-width: 460px;
    }
    .login-card {
        background: rgba(17, 34, 49, 0.95);
        border: 1px solid rgba(0, 194, 255, 0.25);
        border-radius: 12px;
        padding: 42px;
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.45);
    }
    .login-card-title {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .login-card-sub {
        color: #7C8FA3;
        font-size: 0.9rem;
        margin-bottom: 28px;
    }
    .login-footer {
        text-align: center;
        color: #7C8FA3;
        font-size: 12px;
        margin-top: 28px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown(
            """
            <div style="padding: 40px 20px 0 0;">
                <div class="login-hero">
                    AVIONAV<br>
                    <span>Intelligent UAV</span><br>
                    Health Monitoring
                </div>
                <div class="login-sub">
                    Real-time telemetry monitoring and AI-driven anomaly detection
                    for UAV propulsion systems. Predictive maintenance for
                    brushless DC motor bearing wear.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if LOGO.exists():
            st.image(Image.open(LOGO), width=220)

    with col2:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        st.markdown('<div class="login-card-title">Secure Login</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="login-card-sub">Enter your credentials to access the platform</div>',
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
        remember = st.checkbox("Remember me", key="login_remember")

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

        st.markdown(
            '<div class="login-footer">© 2026 AVIONAV · v1.0.0</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
