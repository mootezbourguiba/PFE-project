"""
Header Component Module

This module provides a professional header with page title, user info, and current time.
"""

import streamlit as st
from datetime import datetime
from frontend.utils.auth import (
    is_authenticated,
    current_user,
    get_role_display_name,
    get_role_icon
)


def render_header(page_title: str) -> None:
    """
    Render the professional header with page information.
    
    Args:
        page_title: Title of the current page
    """
    if is_authenticated():
        user = current_user()
        role_icon = get_role_icon(user['role'])
        role_name = get_role_display_name(user['role'])
        current_time = datetime.now().strftime("%H:%M:%S")
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                   padding: 20px 30px; border-radius: 15px; margin-bottom: 20px;
                   display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 style='color: #ffffff; margin: 0; font-size: 24px;'>{page_title}</h1>
                <p style='color: #8892b0; margin: 5px 0 0 0; font-size: 14px;'>AVIONAV Platform</p>
            </div>
            <div style='text-align: right;'>
                <div style='color: #00d4ff; font-size: 18px; font-weight: bold;'>
                    {current_time}
                </div>
                <div style='color: #ffffff; font-size: 14px; margin-top: 5px;'>
                    {role_icon} {user['username']} • {role_name}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                   padding: 20px 30px; border-radius: 15px; margin-bottom: 20px;'>
            <h1 style='color: #ffffff; margin: 0; font-size: 24px;'>{page_title}</h1>
            <p style='color: #8892b0; margin: 5px 0 0 0; font-size: 14px;'>AVIONAV Platform</p>
        </div>
        """, unsafe_allow_html=True)
