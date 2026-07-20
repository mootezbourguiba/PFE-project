"""
Maintenance Engineer Dashboard Module

This module provides the main dashboard for maintenance engineers with:
- Current flight status
- Health monitoring
- Motor telemetry
- AI predictions
- Anomaly detection
"""

import streamlit as st
import numpy as np
from frontend.utils.auth import require_maintenance_engineer, init_session_state
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import metric_card, status_card, alert_card
from frontend.components.charts import line_chart
from frontend.components.gauges import gauge_chart, health_gauge
from frontend.utils.api import predict_anomaly


def show() -> None:
    """
    Display the Maintenance Engineer dashboard.
    
    This function renders:
    - Current flight information
    - Health score
    - Motor current and temperature
    - Battery status
    - AI prediction results
    - Recent alerts
    - System status
    """
    # Initialize session state and require authentication
    init_session_state()
    require_maintenance_engineer()
    
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
    render_header("Maintenance Dashboard")
    
    # Current flight status
    st.markdown("### Current Flight Status")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Flight ID", "FLT-2026-001", "✈️", "#00d4ff")
    
    with col2:
        metric_card("Duration", "00:45:23", "⏱️", "#00ff88")
    
    with col3:
        metric_card("Altitude", "150m", "📏", "#ff9800")
    
    with col4:
        metric_card("Speed", "12 m/s", "🚀", "#9c27b0")
    
    st.markdown("---")
    
    # Health and telemetry gauges
    col1, col2, col3 = st.columns(3)
    
    with col1:
        health_gauge("Overall Health Score", 85)
    
    with col2:
        gauge_chart("Motor Current (A)", 2.5, 0, 5, "A", "#00d4ff")
    
    with col3:
        gauge_chart("Motor Temperature (°C)", 45, 0, 100, "°C", "#ff9800")
    
    st.markdown("---")
    
    # AI Prediction section
    st.markdown("### AI Anomaly Detection")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Predict Anomaly")
        with st.form("predict_form"):
            current_input = st.slider("Motor Current (A)", 0.0, 5.0, 2.5, 0.1)
            temp_input = st.slider("Motor Temperature (°C)", 0.0, 100.0, 45.0, 1.0)
            
            predict_button = st.form_submit_button("Run Prediction", type="primary")
            
            if predict_button:
                result = predict_anomaly(current_input, temp_input)
                
                if result:
                    prediction = result.get("prediction", "unknown")
                    score = result.get("score", 0.0)
                    
                    if prediction == "anomaly":
                        alert_card(
                            "Anomaly Detected",
                            f"AI model detected an anomaly with confidence score: {score:.2f}. Immediate inspection recommended.",
                            "error"
                        )
                    else:
                        alert_card(
                            "Normal Operation",
                            f"AI model indicates normal operation with confidence score: {score:.2f}.",
                            "success"
                        )
                else:
                    st.error("Failed to get prediction from backend.")
    
    with col2:
        st.markdown("#### AI Model Information")
        info_card(
            "Isolation Forest Model",
            "The AI model uses Isolation Forest algorithm to detect anomalies in UAV motor telemetry data. It analyzes current and temperature patterns to identify potential bearing wear or motor failures.",
            "🤖"
        )
    
    st.markdown("---")
    
    # Historical telemetry chart
    st.markdown("### Historical Telemetry")
    col1, col2 = st.columns(2)
    
    with col1:
        # Generate sample historical data
        time_points = list(range(50))
        current_data = [2.0 + 0.3 * np.sin(i/5) + 0.1 * np.random.randn() for i in time_points]
        line_chart("Motor Current History", time_points, current_data, "Time (s)", "Current (A)", "#00d4ff")
    
    with col2:
        temp_data = [40 + 5 * np.sin(i/5) + 2 * np.random.randn() for i in time_points]
        line_chart("Motor Temperature History", time_points, temp_data, "Time (s)", "Temperature (°C)", "#ff9800")
    
    st.markdown("---")
    
    # System status and alerts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### System Status")
        status_card("Motor 1", "Normal", "✅", True)
        status_card("Motor 2", "Normal", "✅", True)
        status_card("Battery", "Good", "✅", True)
        status_card("GPS", "Connected", "✅", True)
    
    with col2:
        st.markdown("### Recent Alerts")
        alert_card(
            "No Active Alerts",
            "All systems are operating within normal parameters. No anomalies detected in the last 24 hours.",
            "success"
        )
