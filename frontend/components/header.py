"""
Header Component

Professional top header for AVIONAV pages.
"""

import streamlit as st
from datetime import datetime
from utils.auth import current_user, current_role, get_role_display_name, get_role_icon
from components.theme import COLORS, header_style


def show(title: str, subtitle: str = "") -> None:
    """
    Display the page header.
    """
    st.markdown(header_style(), unsafe_allow_html=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user = current_user() or "Guest"
    role = current_role() or ""
    role_display = get_role_display_name(role) if role else ""

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"""
            <div class="avionav-header">
                <div>
                    <div class="avionav-header-title">{title}</div>
                    {f'<div class="avionav-header-subtitle">{subtitle}</div>' if subtitle else ''}
                </div>
                <div class="avionav-header-meta">
                    <div style="margin-bottom: 4px;">
                        <span class="avionav-status-dot" style="background: {COLORS['success']};"></span>
                        SYSTEM OPERATIONAL
                    </div>
                    <div style="color: {COLORS['primary']}; font-weight: 600;">{get_role_icon(role)} {role_display}</div>
                    <div>{user}</div>
                    <div style="color: {COLORS['text_muted']}; margin-top: 2px;">{current_time}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
