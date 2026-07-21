"""
Header Component

This module provides a professional header component for the application.
"""

import streamlit as st
from datetime import datetime
from utils.auth import current_user, current_role, get_role_display_name


def render_header(page_title: str) -> None:
    """
    Render the professional header with page title and user info.
    
    Args:
        page_title: Title of the current page
    """
    # Current time
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px 30px; border-radius: 10px; margin-bottom: 20px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 style='color: #FFFFFF; font-size: 24px; margin: 0;'>{page_title}</h1>
                <p style='color: #B0B0B0; font-size: 12px; margin: 5px 0;'>{current_date} • {current_time}</p>
            </div>
            <div style='text-align: right;'>
                <p style='color: #00D4FF; font-size: 14px; margin: 0;'>{current_user() if current_user() else 'Guest'}</p>
                <p style='color: #808080; font-size: 11px; margin: 5px 0;'>{get_role_display_name(current_role()) if current_role() else 'Not authenticated'}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
