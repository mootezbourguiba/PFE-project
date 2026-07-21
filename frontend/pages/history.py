"""
History Page

This module provides the flight and telemetry history interface.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.auth import require_authentication, init_session_state
from components.sidebar import render_sidebar
from components.header import render_header
from components.cards import metric_card
from components.charts import bar_chart, line_chart


def show() -> None:
    """
    Display the history page.
    """
    # Initialize session state and require authentication
    init_session_state()
    require_authentication()
    
    # Page configuration
    st.set_page_config(
        page_title="History",
        page_icon="📜",
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
    render_header("Flight & Telemetry History")
    
    # Tabs for different history views
    tab1, tab2, tab3 = st.tabs(["✈ Flight History", "📊 Telemetry History", "🚨 Alert History"])
    
    # Tab 1: Flight History
    with tab1:
        st.markdown("### Flight History")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", pd.to_datetime('2026-07-01'))
        with col2:
            end_date = st.date_input("End Date", pd.to_datetime('2026-07-21'))
        
        st.markdown("---")
        
        # Flight statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Total Flights", "24", "✈", "#00D4FF")
        
        with col2:
            metric_card("Total Hours", "18.5", "⏱", "#00FF00")
        
        with col3:
            metric_card("Avg Duration", "46 min", "📏", "#FFA500")
        
        with col4:
            metric_card("Success Rate", "95.8%", "✅", "#FF00FF")
        
        st.markdown("---")
        
        # Flight history table
        st.markdown("### Flight Records")
        
        # Generate sample flight data
        flight_data = pd.DataFrame({
            'Flight ID': [f'FLT-2026-{i:03d}' for i in range(1, 11)],
            'Date': pd.date_range(start=start_date, periods=10, freq='2D'),
            'Duration (min)': np.random.randint(30, 60, 10),
            'Distance (km)': np.random.randint(2, 5, 10),
            'Status': ['Completed'] * 9 + ['Aborted'],
            'Health Score': np.random.randint(80, 100, 10)
        })
        
        st.dataframe(flight_data, use_container_width=True)
    
    # Tab 2: Telemetry History
    with tab2:
        st.markdown("### Telemetry History")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            flight_id = st.selectbox("Select Flight", [f'FLT-2026-{i:03d}' for i in range(1, 11)])
        with col2:
            metric_type = st.selectbox("Metric Type", ["Motor Current", "Temperature", "Battery", "RPM"])
        
        st.markdown("---")
        
        # Telemetry chart
        time_data = pd.date_range(start='2026-07-21 10:00:00', periods=50, freq='1min')
        
        if metric_type == "Motor Current":
            data = np.random.normal(12, 2, 50)
            chart_data = pd.DataFrame({'Time': time_data, 'Motor Current (A)': data})
            line_chart(f"Motor Current - {flight_id}", chart_data, 'Time', 'Motor Current (A)', "#00D4FF")
        elif metric_type == "Temperature":
            data = np.random.normal(60, 8, 50)
            chart_data = pd.DataFrame({'Time': time_data, 'Temperature (°C)': data})
            line_chart(f"Temperature - {flight_id}", chart_data, 'Time', 'Temperature (°C)', "#FFA500")
        elif metric_type == "Battery":
            data = np.random.normal(75, 10, 50)
            chart_data = pd.DataFrame({'Time': time_data, 'Battery (%)': data})
            line_chart(f"Battery Level - {flight_id}", chart_data, 'Time', 'Battery (%)', "#00FF00")
        else:
            data = np.random.normal(4200, 200, 50)
            chart_data = pd.DataFrame({'Time': time_data, 'RPM': data})
            line_chart(f"RPM - {flight_id}", chart_data, 'Time', 'RPM', "#FF00FF")
        
        st.markdown("---")
        
        # Telemetry statistics
        st.markdown("### Telemetry Statistics")
        stats_data = pd.DataFrame({
            'Metric': ['Avg Current', 'Max Current', 'Avg Temperature', 'Max Temperature', 'Avg Battery', 'Min Battery'],
            'Value': [12.3, 15.2, 62.5, 78.3, 76.2, 45.1],
            'Unit': ['A', 'A', '°C', '°C', '%', '%']
        })
        st.dataframe(stats_data, use_container_width=True)
    
    # Tab 3: Alert History
    with tab3:
        st.markdown("### Alert History")
        
        # Alert statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            metric_card("Total Alerts", "15", "🚨", "#FF0000")
        
        with col2:
            metric_card("Warnings", "12", "⚠️", "#FFA500")
        
        with col3:
            metric_card("Critical", "3", "❌", "#FF0000")
        
        st.markdown("---")
        
        # Alert history table
        st.markdown("### Alert Records")
        
        # Generate sample alert data
        alert_data = pd.DataFrame({
            'Timestamp': pd.date_range(start='2026-07-21 10:00:00', periods=10, freq='30min'),
            'Type': ['Warning', 'Warning', 'Critical', 'Warning', 'Warning', 'Critical', 'Warning', 'Warning', 'Warning', 'Critical'],
            'Message': [
                'Motor 2 temperature high',
                'Battery level low',
                'Motor 1 current spike',
                'Motor 3 temperature warning',
                'Battery level warning',
                'Motor 2 failure detected',
                'Motor 1 temperature warning',
                'Battery level low',
                'Motor 3 current warning',
                'Communication loss'
            ],
            'Status': ['Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved', 'Resolved']
        })
        
        st.dataframe(alert_data, use_container_width=True)
        
        st.markdown("---")
        
        # Alert distribution chart
        alert_counts = pd.DataFrame({
            'Type': ['Warning', 'Critical'],
            'Count': [12, 3]
        })
        bar_chart("Alert Distribution", alert_counts, 'Type', 'Count', "#FF0000")
