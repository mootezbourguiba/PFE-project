"""
Drone Operator Dashboard Page

This module provides the drone operator dashboard with simplified interface for real-time monitoring.
"""

import streamlit as st
from utils.auth import require_authentication, init_session_state
from components.sidebar import render_sidebar
from components.header import render_header
from components.cards import metric_card, status_card, alert_card
from components.gauges import health_gauge, temperature_gauge, battery_gauge


def show() -> None:
    """
    Display the drone operator dashboard.
    """
    # Initialize session state and require authentication
    init_session_state()
    require_authentication()
    
    # Page configuration
    st.set_page_config(
        page_title="Operator Dashboard",
        page_icon="🚁",
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
    render_header("Drone Operator Dashboard")
    
    # Current mission status
    st.markdown("### Current Mission Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric_card("Mission ID", "MSN-2026-001", "🎯", "#00D4FF")
    
    with col2:
        metric_card("Flight Time", "00:45:23", "⏱", "#00FF00")
    
    with col3:
        metric_card("Distance", "2.5 km", "📍", "#FFA500")
    
    st.markdown("---")
    
    # Health indicators
    col1, col2, col3 = st.columns(3)
    
    with col1:
        health_gauge("Overall Health", 92)
    
    with col2:
        temperature_gauge("Motor Temperature", 58, min_temp=0, max_temp=100)
    
    with col3:
        battery_gauge("Battery Level", 85)
    
    st.markdown("---")
    
    # Motor status
    st.markdown("### Motor Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_card("Motor 1", "Normal", "#00FF00")
    
    with col2:
        status_card("Motor 2", "Normal", "#00FF00")
    
    with col3:
        status_card("Motor 3", "Normal", "#00FF00")
    
    st.markdown("---")
    
    # Quick metrics
    st.markdown("### Quick Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_card("Current", "11.2 A", "⚡", "#00D4FF")
    
    with col2:
        metric_card("Temperature", "58°C", "🌡", "#00FF00")
    
    st.markdown("---")
    
    # Alerts
    st.markdown("### Alerts")
    
    alert_card(
        "No Active Alerts",
        "All systems operating within normal parameters.",
        "success"
    )
    
    st.markdown("---")
    
    # Emergency warning (placeholder)
    st.markdown("### Emergency Status")
    
    status_card("Emergency Mode", "Inactive", "#00FF00")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 View Telemetry", use_container_width=True, key="quick_telemetry"):
            st.session_state.current_page = "telemetry"
            st.rerun()
    
    with col2:
        if st.button("⚙️ Settings", use_container_width=True, key="quick_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
