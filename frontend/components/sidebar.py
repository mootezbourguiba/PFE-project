"""
Sidebar Component

Professional AVIONAV navigation sidebar.
"""

import streamlit as st
from pathlib import Path
from PIL import Image
from utils.auth import current_user, current_role, get_role_icon, get_role_display_name, logout
from components.theme import COLORS


def _nav_item(page_key: str, icon: str, label: str, current_page: str) -> None:
    is_active = current_page == page_key

    if is_active:
        st.markdown(
            f"""
            <div style="
                background: rgba(0, 194, 255, 0.10);
                border-left: 3px solid {COLORS['primary']};
                border-radius: 0 6px 6px 0;
                padding: 10px 14px;
                margin: 2px -16px;
                color: {COLORS['white']};
                font-weight: 600;
                font-size: 14px;
                display: flex;
                align-items: center;
            ">
                <span style="margin-right: 10px; color: {COLORS['primary']};">{icon}</span>
                {label}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        if st.button(
            f"{icon}  {label}",
            key=f"nav_{page_key}",
            use_container_width=True,
        ):
            st.session_state.current_page = page_key
            st.rerun()


def show(page: str = "dashboard") -> None:
    """Display the AVIONAV sidebar."""
    with st.sidebar:
        # Branding
        BASE_DIR = Path(__file__).parent.parent
        LOGO = BASE_DIR / "assets" / "images" / "avionav_logo.png"

        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0 4px 0;">
            <div style="
                color: {COLORS['primary']};
                font-size: 22px;
                font-weight: 700;
                letter-spacing: 1px;
            ">✈️ AVIONAV</div>
            <div style="
                color: {COLORS['text_muted']};
                font-size: 10px;
                letter-spacing: 0.8px;
                text-transform: uppercase;
                margin-top: 4px;
            ">Intelligent UAV Health</div>
            <div style="
                color: {COLORS['text_muted']};
                font-size: 10px;
                letter-spacing: 0.8px;
                text-transform: uppercase;
            ">Monitoring</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation
        st.markdown(f"""
        <div style="
            color: {COLORS['text_muted']};
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 10px;
            padding-left: 4px;
        ">Navigation</div>
        """, unsafe_allow_html=True)

        role = current_role()

        if role == "administrator":
            _admin_navigation(page)
        elif role == "maintenance_engineer":
            _maintenance_navigation(page)
        elif role == "drone_operator":
            _operator_navigation(page)

        st.markdown("---")

        # User footer
        if current_user():
            st.markdown(f"""
            <div style="
                background: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 12px;
                margin-bottom: 12px;
            ">
                <div style="color: {COLORS['white']}; font-weight: 600; font-size: 14px;">
                    {get_role_icon(role)} {current_user()}
                </div>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">
                    {get_role_display_name(role)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🚪  Logout", key="sidebar_logout_button", use_container_width=True):
            logout()


def _admin_navigation(current_page: str) -> None:
    _nav_item("dashboard_admin", "🏠", "Dashboard", current_page)
    _nav_item("users", "👥", "Users", current_page)
    _nav_item("settings", "⚙", "Settings", current_page)


def _maintenance_navigation(current_page: str) -> None:
    _nav_item("dashboard_maintenance", "🏠", "Dashboard", current_page)
    _nav_item("telemetry", "�", "Telemetry", current_page)
    _nav_item("history", "�", "History", current_page)
    _nav_item("settings", "⚙", "Settings", current_page)


def _operator_navigation(current_page: str) -> None:
    _nav_item("dashboard_operator", "🏠", "Dashboard", current_page)
