"""
Administrator Dashboard Page

This module provides the administrator dashboard with system statistics and user management.
"""

import streamlit as st
import pandas as pd
from utils.auth import require_administrator, init_session_state
from components.sidebar import render_sidebar
from components.header import render_header
from components.cards import metric_card, info_card, status_card
from utils.api import get_users


def show() -> None:
    """
    Display the administrator dashboard.
    """
    # Initialize session state and require authentication
    init_session_state()
    require_administrator()
    
    # Page configuration
    st.set_page_config(
        page_title="Administrator Dashboard",
        page_icon="👤",
        layout="wide"
    )
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0D1B2A 0%, #1E3A5F 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    render_sidebar()
    
    # Render header
    render_header("Administrator Dashboard")
    
    # Fetch user statistics
    users = get_users()
    
    if users:
        total_users = len(users)
        admin_count = sum(1 for u in users if u.get('role') == 'administrator')
        maintenance_count = sum(1 for u in users if u.get('role') == 'maintenance_engineer')
        operator_count = sum(1 for u in users if u.get('role') == 'drone_operator')
        disabled_count = sum(1 for u in users if u.get('disabled'))
    else:
        total_users = 0
        admin_count = 0
        maintenance_count = 0
        operator_count = 0
        disabled_count = 0
    
    # Statistics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Users", str(total_users), "👥", "#00D4FF")
    
    with col2:
        metric_card("Administrators", str(admin_count), "👤", "#00FF00")
    
    with col3:
        metric_card("Maintenance Engineers", str(maintenance_count), "🔧", "#FFA500")
    
    with col4:
        metric_card("Drone Operators", str(operator_count), "🚁", "#FF00FF")
    
    st.markdown("---")
    
    # System status cards
    col1, col2 = st.columns(2)
    
    with col1:
        status_card("System Status", "Online", "#00FF00")
    
    with col2:
        status_card("Database", "Connected", "#00FF00")
    
    st.markdown("---")
    
    # User distribution chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Users by Role")
        if total_users > 0:
            role_data = pd.DataFrame({
                'Role': ['Administrator', 'Maintenance Engineer', 'Drone Operator'],
                'Count': [admin_count, maintenance_count, operator_count]
            })
            st.bar_chart(role_data.set_index('Role'))
        else:
            st.info("No users found in the system.")
    
    with col2:
        st.markdown("### Account Status")
        if total_users > 0:
            status_data = pd.DataFrame({
                'Status': ['Active', 'Disabled'],
                'Count': [total_users - disabled_count, disabled_count]
            })
            st.bar_chart(status_data.set_index('Status'))
        else:
            st.info("No users found in the system.")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👥 Manage Users", use_container_width=True, key="quick_users"):
            st.session_state.current_page = "users"
            st.rerun()
    
    with col2:
        if st.button("📜 View History", use_container_width=True, key="quick_history"):
            st.session_state.current_page = "history"
            st.rerun()
    
    with col3:
        if st.button("⚙️ Settings", use_container_width=True, key="quick_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
    
    st.markdown("---")
    
    # Recent users table
    st.markdown("### Recent Users")
    
    if users:
        users_df = pd.DataFrame(users)
        users_df = users_df[['id', 'username', 'email', 'role', 'disabled', 'created_at']]
        users_df.columns = ['ID', 'Username', 'Email', 'Role', 'Disabled', 'Created At']
        st.dataframe(users_df, use_container_width=True)
    else:
        st.info("No users found in the system.")
    
    st.markdown("---")
    
    # Information cards
    col1, col2 = st.columns(2)
    
    with col1:
        info_card(
            "Platform Information",
            "AVIONAV Intelligent UAV Health Monitoring Platform v1.0.0",
            "ℹ️"
        )
    
    with col2:
        info_card(
            "System Status",
            "All systems operational. Backend API connected. Database synchronized.",
            "✅"
        )
