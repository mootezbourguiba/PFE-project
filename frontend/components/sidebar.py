"""
Sidebar Component

This module provides a professional sidebar component for navigation.
"""

import streamlit as st
from utils.auth import current_user, current_role, get_role_display_name, get_role_icon, logout


def render_sidebar() -> None:
    """
    Render the professional sidebar with navigation.
    """
    with st.sidebar:
        # Logo and Brand
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #00D4FF; font-size: 28px; margin: 0;'>✈ AVIONAV</h1>
            <p style='color: #B0B0B0; font-size: 12px; margin: 5px 0;'>Intelligent UAV Health Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User Information
        if current_user():
            role_icon = get_role_icon(current_role())
            role_name = get_role_display_name(current_role())
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
                       padding: 15px; border-radius: 10px; margin: 10px 0;'>
                <div style='display: flex; align-items: center; gap: 10px;'>
                    <span style='font-size: 24px;'>{role_icon}</span>
                    <div>
                        <div style='color: #FFFFFF; font-weight: bold; font-size: 14px;'>{current_user()}</div>
                        <div style='color: #00D4FF; font-size: 11px;'>{role_name}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### Navigation")
        
        # Dashboard
        if current_role() == "administrator":
            if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard_admin"
                st.rerun()
        elif current_role() == "maintenance_engineer":
            if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard_maintenance"
                st.rerun()
        elif current_role() == "drone_operator":
            if st.button("📊 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard_operator"
                st.rerun()
        
        # Users (Admin only)
        if current_role() == "administrator":
            if st.button("👥 Users", key="nav_users", use_container_width=True):
                st.session_state.current_page = "users"
                st.rerun()
        
        # Telemetry
        if current_role() in ["maintenance_engineer", "drone_operator"]:
            if st.button("📈 Telemetry", key="nav_telemetry", use_container_width=True):
                st.session_state.current_page = "telemetry"
                st.rerun()
        
        # History
        if current_role() in ["maintenance_engineer", "administrator"]:
            if st.button("📜 History", key="nav_history", use_container_width=True):
                st.session_state.current_page = "history"
                st.rerun()
        
        # Settings
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True, type="secondary"):
            logout()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; padding: 10px;'>
            <p style='color: #606060; font-size: 10px; margin: 0;'>Version 1.0.0</p>
            <p style='color: #404040; font-size: 9px; margin: 5px 0;'>© 2026 AVIONAV</p>
        </div>
        """, unsafe_allow_html=True)
