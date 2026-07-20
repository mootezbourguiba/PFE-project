"""
Sidebar Component Module

This module provides a professional sidebar for navigation with role-based menu items.
"""

import streamlit as st
from frontend.utils.auth import (
    is_authenticated,
    current_user,
    current_role,
    get_role_display_name,
    get_role_icon,
    logout,
    is_administrator,
    is_maintenance_engineer,
    is_drone_operator
)


def render_sidebar() -> None:
    """
    Render the professional sidebar with navigation and user information.
    
    This function displays:
    - Logo and branding
    - Role-based navigation menu
    - Current user information
    - Logout button
    """
    with st.sidebar:
        # Logo and branding
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #00d4ff; font-size: 28px; margin: 0;'>AVIONAV</h1>
            <p style='color: #8892b0; font-size: 12px; margin: 5px 0;'>Intelligent UAV Health Monitoring</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu based on role
        if is_authenticated():
            user_role = current_role()
            
            st.markdown("### Navigation")
            st.markdown("---")
            
            # Common navigation
            if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
            
            # Administrator navigation
            if is_administrator():
                if st.button("👤 Users", key="nav_users", use_container_width=True):
                    st.session_state.page = "users"
                    st.rerun()
                
                if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
                    st.session_state.page = "settings"
                    st.rerun()
            
            # Maintenance Engineer navigation
            if is_maintenance_engineer():
                if st.button("📈 Telemetry", key="nav_telemetry", use_container_width=True):
                    st.session_state.page = "telemetry"
                    st.rerun()
                
                if st.button("📜 History", key="nav_history", use_container_width=True):
                    st.session_state.page = "history"
                    st.rerun()
            
            # Drone Operator navigation
            if is_drone_operator():
                if st.button("📈 Telemetry", key="nav_telemetry", use_container_width=True):
                    st.session_state.page = "telemetry"
                    st.rerun()
            
            st.markdown("---")
            
            # User information section
            user = current_user()
            if user:
                st.markdown("### User Profile")
                st.markdown("---")
                
                role_icon = get_role_icon(user_role)
                role_name = get_role_display_name(user_role)
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                           padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <div style='display: flex; align-items: center; gap: 10px;'>
                        <span style='font-size: 24px;'>{role_icon}</span>
                        <div>
                            <div style='color: #ffffff; font-weight: bold; font-size: 14px;'>
                                {user['username']}
                            </div>
                            <div style='color: #00d4ff; font-size: 12px;'>
                                {role_name}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Logout button
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True, type="secondary"):
                logout()
        
        else:
            # Not authenticated - show login prompt
            st.markdown("### Please Login")
            st.markdown("---")
            st.info("Login to access the dashboard")
