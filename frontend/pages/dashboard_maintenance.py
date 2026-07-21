"""
Maintenance Engineer Dashboard Page

This module provides the maintenance engineer dashboard with health monitoring and AI predictions.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.auth import require_authentication, init_session_state, is_maintenance_engineer
from components.sidebar import render_sidebar
from components.header import render_header
from components.cards import metric_card, status_card, alert_card, prediction_card
from components.charts import line_chart, multi_line_chart
from components.gauges import health_gauge, temperature_gauge, battery_gauge


def show() -> None:
    """
    Display the maintenance engineer dashboard.
    """
    # Initialize session state and require authentication
    init_session_state()
    require_authentication()
    
    # Page configuration
    st.set_page_config(
        page_title="Maintenance Dashboard",
        page_icon="🔧",
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
    render_header("Maintenance Engineer Dashboard")
    
    # Current flight information
    st.markdown("### Current Flight Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Flight ID", "FLT-2026-001", "✈", "#00D4FF")
    
    with col2:
        metric_card("Duration", "00:45:23", "⏱", "#00FF00")
    
    with col3:
        metric_card("Altitude", "1,250 m", "📏", "#FFA500")
    
    with col4:
        metric_card("Speed", "45 km/h", "🚀", "#FF00FF")
    
    st.markdown("---")
    
    # Health score and gauges
    col1, col2, col3 = st.columns(3)
    
    with col1:
        health_gauge("Overall Health Score", 87)
    
    with col2:
        temperature_gauge("Motor Temperature", 65, min_temp=0, max_temp=100)
    
    with col3:
        battery_gauge("Battery Level", 78)
    
    st.markdown("---")
    
    # Motor metrics
    st.markdown("### Motor Telemetry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        metric_card("Motor Current", "12.5 A", "⚡", "#00D4FF")
    
    with col2:
        metric_card("Motor RPM", "4,500", "🔄", "#00FF00")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate sample data for motor current
        time_data = pd.date_range(start='2026-07-21 10:00:00', periods=20, freq='1min')
        current_data = np.random.normal(12, 2, 20)
        chart_data = pd.DataFrame({'Time': time_data, 'Current (A)': current_data})
        line_chart("Motor Current Over Time", chart_data, 'Time', 'Current (A)', "#00D4FF")
    
    with col2:
        # Generate sample data for temperature
        temp_data = np.random.normal(65, 5, 20)
        chart_data = pd.DataFrame({'Time': time_data, 'Temperature (°C)': temp_data})
        line_chart("Motor Temperature Over Time", chart_data, 'Time', 'Temperature (°C)', "#FFA500")
    
    st.markdown("---")
    
    # AI Prediction
    st.markdown("### AI Anomaly Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        prediction_card(
            "Isolation Forest Model",
            "Normal Operation",
            92.5,
            "Continue monitoring. No maintenance required."
        )
    
    with col2:
        status_card("AI Model Status", "Active", "#00FF00")
    
    st.markdown("---")
    
    # Recent alerts
    st.markdown("### Recent Alerts")
    
    alert_card(
        "Motor Temperature Warning",
        "Motor 2 temperature approaching threshold (65°C). Monitor closely.",
        "warning"
    )
    
    st.markdown("---")
    
    # System status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status_card("Motor 1", "Normal", "#00FF00")
    
    with col2:
        status_card("Motor 2", "Warning", "#FFA500")
    
    with col3:
        status_card("Motor 3", "Normal", "#00FF00")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📈 View Telemetry", use_container_width=True, key="quick_telemetry"):
            st.session_state.current_page = "telemetry"
            st.rerun()
    
    with col2:
        if st.button("📜 View History", use_container_width=True, key="quick_history"):
            st.session_state.current_page = "history"
            st.rerun()
    
    with col3:
        if st.button("⚙️ Settings", use_container_width=True, key="quick_settings"):
            st.session_state.current_page = "settings"
            st.rerun()
