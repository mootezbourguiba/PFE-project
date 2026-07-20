"""
History Page Module

This module provides historical data viewing including:
- Flight history
- Telemetry history
- Predictions history
- Alerts history
- Filtering and search
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from frontend.utils.auth import require_authentication, init_session_state
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import metric_card, info_card
from frontend.components.charts import line_chart, bar_chart


def show() -> None:
    """
    Display the History page.
    
    This function renders:
    - Flight history
    - Telemetry history
    - Predictions history
    - Alerts history
    - Filtering and search capabilities
    """
    # Initialize session state and require authentication
    init_session_state()
    require_authentication()
    
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
    render_header("Historical Data")
    
    # Tabs for different history views
    tab1, tab2, tab3, tab4 = st.tabs(["✈️ Flight History", "📈 Telemetry History", "🤖 Predictions", "🚨 Alerts"])
    
    # Tab 1: Flight History
    with tab1:
        st.markdown("### Flight History")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_range = st.date_input(
                "Date Range",
                value=(datetime.now() - timedelta(days=30), datetime.now()),
                max_value=datetime.now()
            )
        
        with col2:
            status_filter = st.selectbox("Flight Status", ["All", "Completed", "In Progress", "Failed"])
        
        with col3:
            search_flight = st.text_input("Search Flight ID", placeholder="Enter flight ID")
        
        st.markdown("---")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Total Flights", "24", "✈️", "#00d4ff")
        
        with col2:
            metric_card("Completed", "22", "✅", "#00ff88")
        
        with col3:
            metric_card("In Progress", "1", "🔄", "#ff9800")
        
        with col4:
            metric_card("Failed", "1", "❌", "#ff4444")
        
        st.markdown("---")
        
        # Flight history table (sample data)
        flight_data = {
            "Flight ID": ["FLT-2026-001", "FLT-2026-002", "FLT-2026-003", "FLT-2026-004", "FLT-2026-005"],
            "Date": ["2026-07-15", "2026-07-16", "2026-07-17", "2026-07-18", "2026-07-19"],
            "Duration": ["01:23:45", "00:45:30", "02:15:20", "01:05:10", "00:58:45"],
            "Status": ["Completed", "Completed", "Completed", "Failed", "In Progress"],
            "Distance (km)": [2.4, 1.8, 3.2, 1.5, 2.1]
        }
        
        df_flights = pd.DataFrame(flight_data)
        st.dataframe(df_flights, use_container_width=True, hide_index=True)
    
    # Tab 2: Telemetry History
    with tab2:
        st.markdown("### Telemetry History")
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            telemetry_date = st.date_input("Select Date", value=datetime.now())
        
        with col2:
            motor_select = st.selectbox("Select Motor", ["All", "Motor 1", "Motor 2", "Motor 3", "Motor 4"])
        
        st.markdown("---")
        
        # Historical telemetry charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate sample historical data
            time_points = list(range(100))
            current_data = [2.0 + 0.5 * np.sin(i/10) + 0.3 * np.random.randn() for i in time_points]
            line_chart("Motor Current History", time_points, current_data, "Time (s)", "Current (A)", "#00d4ff")
        
        with col2:
            temp_data = [40 + 10 * np.sin(i/10) + 4 * np.random.randn() for i in time_points]
            line_chart("Motor Temperature History", time_points, temp_data, "Time (s)", "Temperature (°C)", "#ff9800")
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### Telemetry Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Avg Current", "2.3 A", "⚡", "#00d4ff")
        
        with col2:
            metric_card("Avg Temperature", "42°C", "🌡️", "#ff9800")
        
        with col3:
            metric_card("Max Current", "3.8 A", "⚡", "#00d4ff")
        
        with col4:
            metric_card("Max Temperature", "58°C", "🌡️", "#ff9800")
    
    # Tab 3: Predictions
    with tab3:
        st.markdown("### AI Prediction History")
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            prediction_date = st.date_input("Prediction Date", value=datetime.now())
        
        with col2:
            result_filter = st.selectbox("Prediction Result", ["All", "Normal", "Anomaly"])
        
        st.markdown("---")
        
        # Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            metric_card("Total Predictions", "156", "🤖", "#9c27b0")
        
        with col2:
            metric_card("Normal", "142", "✅", "#00ff88")
        
        with col3:
            metric_card("Anomalies", "14", "⚠️", "#ff9800")
        
        st.markdown("---")
        
        # Prediction history chart
        prediction_counts = [12, 15, 8, 10, 14, 11, 13, 9, 16, 12]
        days = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Day 8", "Day 9", "Day 10"]
        bar_chart("Predictions per Day", days, prediction_counts, "#9c27b0")
        
        st.markdown("---")
        
        # Prediction history table
        prediction_data = {
            "Timestamp": ["2026-07-19 10:30", "2026-07-19 11:15", "2026-07-19 12:00", "2026-07-19 13:45", "2026-07-19 14:30"],
            "Current (A)": [2.3, 2.5, 3.8, 2.1, 2.4],
            "Temperature (°C)": [42, 45, 58, 40, 43],
            "Result": ["Normal", "Normal", "Anomaly", "Normal", "Normal"],
            "Confidence": [0.92, 0.88, 0.95, 0.91, 0.89]
        }
        
        df_predictions = pd.DataFrame(prediction_data)
        st.dataframe(df_predictions, use_container_width=True, hide_index=True)
    
    # Tab 4: Alerts
    with tab4:
        st.markdown("### Alert History")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            alert_date = st.date_input("Alert Date", value=datetime.now())
        
        with col2:
            severity_filter = st.selectbox("Severity", ["All", "Critical", "Warning", "Info"])
        
        with col3:
            alert_type_filter = st.selectbox("Alert Type", ["All", "Motor", "Battery", "GPS", "Communication"])
        
        st.markdown("---")
        
        # Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            metric_card("Total Alerts", "8", "🚨", "#ff4444")
        
        with col2:
            metric_card("Critical", "2", "❌", "#ff4444")
        
        with col3:
            metric_card("Warnings", "6", "⚠️", "#ff9800")
        
        st.markdown("---")
        
        # Alert history table
        alert_data = {
            "Timestamp": ["2026-07-19 09:15", "2026-07-19 10:30", "2026-07-19 11:45", "2026-07-19 13:00", "2026-07-19 14:15"],
            "Type": ["Motor", "Battery", "GPS", "Communication", "Motor"],
            "Severity": ["Critical", "Warning", "Warning", "Info", "Warning"],
            "Message": ["High temperature detected", "Low battery level", "Weak GPS signal", "Connection lost", "Current spike detected"],
            "Status": ["Resolved", "Resolved", "Active", "Resolved", "Active"]
        }
        
        df_alerts = pd.DataFrame(alert_data)
        st.dataframe(df_alerts, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Alert distribution chart
        alert_types = ["Motor", "Battery", "GPS", "Communication"]
        alert_counts = [3, 2, 2, 1]
        bar_chart("Alerts by Type", alert_types, alert_counts, "#ff4444")
