"""
Administrator Dashboard Module

This module provides the main dashboard for administrators with system statistics and quick actions.
"""

import streamlit as st
from frontend.utils.auth import require_administrator, init_session_state
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import metric_card, status_card, info_card
from frontend.components.charts import pie_chart, bar_chart
from frontend.utils.api import get_users


def show() -> None:
    """
    Display the Administrator dashboard.
    
    This function renders:
    - System statistics cards
    - User distribution charts
    - Quick action buttons
    - Recent activity
    """
    # Initialize session state and require authentication
    init_session_state()
    require_administrator()
    
    # Page configuration is handled in app.py
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1e3a5f 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar and header
    render_sidebar()
    render_header("Administrator Dashboard")
    
    # Statistics cards row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Total Users", "3", "👤", "#00d4ff")
    
    with col2:
        metric_card("Active Flights", "0", "✈️", "#00ff88")
    
    with col3:
        metric_card("System Alerts", "0", "🚨", "#ff9800")
    
    with col4:
        metric_card("AI Models", "1", "🤖", "#9c27b0")
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        # User distribution by role
        st.markdown("### Users by Role")
        pie_chart(
            "User Distribution",
            ["Administrator", "Maintenance Engineer", "Drone Operator"],
            [1, 1, 1],
            ["#00d4ff", "#00ff88", "#ff9800"]
        )
    
    with col2:
        # System status
        st.markdown("### System Status")
        status_card("Backend API", "Online", "✅", True)
        status_card("Database", "Connected", "✅", True)
        status_card("AI Model", "Ready", "✅", True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👤 Manage Users", use_container_width=True, type="primary"):
            st.session_state.page = "users"
            st.rerun()
    
    with col2:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.page = "settings"
            st.rerun()
    
    with col3:
        if st.button("📊 View Reports", use_container_width=True):
            st.info("Reports feature coming soon")
    
    st.markdown("---")
    
    # Information cards
    st.markdown("### Platform Information")
    col1, col2 = st.columns(2)
    
    with col1:
        info_card(
            "System Architecture",
            "The AVIONAV platform uses FastAPI for the backend, Streamlit for the frontend, and Isolation Forest for anomaly detection in UAV motor telemetry data.",
            "🏗️"
        )
    
    with col2:
        info_card(
            "Security Features",
            "JWT-based authentication with role-based access control (RBAC). All API endpoints are protected and users can only access features based on their assigned role.",
            "🔒"
        )
