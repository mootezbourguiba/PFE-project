"""
Drone Operator Dashboard Module

This module provides a simplified dashboard for drone operators with:
- Motor status
- Temperature monitoring
- Current monitoring
- Warnings
- Mission status
- Emergency warnings
- Health indicator
"""

import streamlit as st
import numpy as np
from frontend.utils.auth import require_drone_operator, init_session_state
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import metric_card, status_card, alert_card
from frontend.components.charts import line_chart
from frontend.components.gauges import gauge_chart, health_gauge


def show() -> None:
    """
    Display the Drone Operator dashboard.
    
    This function renders:
    - Simplified motor status
    - Temperature and current monitoring
    - Warnings and alerts
    - Mission status
    - Emergency warnings
    - Health indicator
    """
    # Initialize session state and require authentication
    init_session_state()
    require_drone_operator()
    
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
    render_header("Drone Operator Dashboard")
    
    # Mission status
    st.markdown("### Mission Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        metric_card("Mission ID", "MSN-2026-042", "🎯", "#00d4ff")
    
    with col2:
        metric_card("Flight Time", "01:23:45", "⏱️", "#00ff88")
    
    with col3:
        metric_card("Distance", "2.4 km", "📏", "#ff9800")
    
    st.markdown("---")
    
    # Motor status
    st.markdown("### Motor Status")
    col1, col2 = st.columns(2)
    
    with col1:
        status_card("Motor 1", "Normal", "✅", True)
        status_card("Motor 2", "Normal", "✅", True)
        status_card("Motor 3", "Normal", "✅", True)
        status_card("Motor 4", "Normal", "✅", True)
    
    with col2:
        gauge_chart("Motor 1 Current (A)", 2.3, 0, 5, "A", "#00d4ff")
        gauge_chart("Motor 1 Temperature (°C)", 38, 0, 100, "°C", "#ff9800")
    
    st.markdown("---")
    
    # Health indicator
    st.markdown("### Overall Health")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        health_gauge("System Health", 92)
    
    with col2:
        gauge_chart("Battery Level (%)", 78, 0, 100, "%", "#00ff88")
    
    with col3:
        gauge_chart("Signal Strength (%)", 95, 0, 100, "%", "#9c27b0")
    
    st.markdown("---")
    
    # Live telemetry
    st.markdown("### Live Telemetry")
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate sample live data
        time_points = list(range(50))
        current_data = [2.0 + 0.3 * np.sin(i/5) + 0.1 * np.random.randn() for i in time_points]
        line_chart("Motor Current (Live)", time_points, current_data, "Time (s)", "Current (A)", "#00d4ff")
    
    with col2:
        temp_data = [35 + 5 * np.sin(i/5) + 2 * np.random.randn() for i in time_points]
        line_chart("Motor Temperature (Live)", time_points, temp_data, "Time (s)", "Temperature (°C)", "#ff9800")
    
    st.markdown("---")
    
    # Warnings and alerts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### System Warnings")
        alert_card(
            "No Active Warnings",
            "All systems are operating within normal parameters. No warnings detected.",
            "success"
        )
    
    with col2:
        st.markdown("### Emergency Status")
        alert_card(
            "No Emergency",
            "No emergency conditions detected. Mission proceeding normally.",
            "success"
        )
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Telemetry", use_container_width=True):
            st.session_state.page = "telemetry"
            st.rerun()
    
    with col2:
        if st.button("📜 View History", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()
    
    with col3:
        if st.button("🚨 Emergency Stop", use_container_width=True, type="secondary"):
            st.warning("Emergency stop activated (simulated)")
