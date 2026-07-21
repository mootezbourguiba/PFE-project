"""
Telemetry Page

This module provides the telemetry monitoring interface for live and historical data.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.auth import require_authentication, init_session_state
from components.sidebar import render_sidebar
from components.header import render_header
from components.cards import metric_card
from components.charts import line_chart, multi_line_chart


def show() -> None:
    """
    Display the telemetry page.
    """
    # Initialize session state and require authentication
    init_session_state()
    require_authentication()
    
    # Page configuration
    st.set_page_config(
        page_title="Telemetry",
        page_icon="📈",
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
    render_header("Telemetry Monitoring")
    
    # Tabs for live and historical telemetry
    tab1, tab2, tab3 = st.tabs(["📡 Live Telemetry", "📊 Historical Data", "📤 Upload CSV"])
    
    # Tab 1: Live Telemetry
    with tab1:
        st.markdown("### Live Telemetry Data")
        
        # Current metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Motor Current", "12.3 A", "⚡", "#00D4FF")
        
        with col2:
            metric_card("Temperature", "62°C", "🌡", "#FFA500")
        
        with col3:
            metric_card("Battery", "76%", "🔋", "#00FF00")
        
        with col4:
            metric_card("RPM", "4,200", "🔄", "#FF00FF")
        
        st.markdown("---")
        
        # Live charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate sample live data
            time_data = pd.date_range(start='2026-07-21 10:00:00', periods=30, freq='10s')
            current_data = np.random.normal(12, 1.5, 30)
            chart_data = pd.DataFrame({'Time': time_data, 'Current (A)': current_data})
            line_chart("Live Motor Current", chart_data, 'Time', 'Current (A)', "#00D4FF")
        
        with col2:
            temp_data = np.random.normal(62, 4, 30)
            chart_data = pd.DataFrame({'Time': time_data, 'Temperature (°C)': temp_data})
            line_chart("Live Temperature", chart_data, 'Time', 'Temperature (°C)', "#FFA500")
        
        st.markdown("---")
        
        # Multi-metric chart
        time_data = pd.date_range(start='2026-07-21 10:00:00', periods=30, freq='10s')
        chart_data = pd.DataFrame({
            'Time': time_data,
            'Motor 1': np.random.normal(12, 1, 30),
            'Motor 2': np.random.normal(11.5, 1, 30),
            'Motor 3': np.random.normal(12.2, 1, 30)
        })
        multi_line_chart("All Motors Current", chart_data, 'Time', ['Motor 1', 'Motor 2', 'Motor 3'])
    
    # Tab 2: Historical Data
    with tab2:
        st.markdown("### Historical Telemetry Data")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", pd.to_datetime('2026-07-01'))
        with col2:
            end_date = st.date_input("End Date", pd.to_datetime('2026-07-21'))
        
        st.markdown("---")
        
        # Historical charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate sample historical data
            time_data = pd.date_range(start=start_date, periods=100, freq='1H')
            current_data = np.random.normal(12, 2, 100)
            chart_data = pd.DataFrame({'Time': time_data, 'Current (A)': current_data})
            line_chart("Historical Motor Current", chart_data, 'Time', 'Current (A)', "#00D4FF")
        
        with col2:
            temp_data = np.random.normal(60, 8, 100)
            chart_data = pd.DataFrame({'Time': time_data, 'Temperature (°C)': temp_data})
            line_chart("Historical Temperature", chart_data, 'Time', 'Temperature (°C)', "#FFA500")
        
        st.markdown("---")
        
        # Data table
        st.markdown("### Telemetry Data Table")
        
        # Generate sample data for table
        sample_data = pd.DataFrame({
            'Timestamp': pd.date_range(start=start_date, periods=10, freq='1H'),
            'Motor 1 Current (A)': np.random.normal(12, 2, 10),
            'Motor 2 Current (A)': np.random.normal(11.5, 2, 10),
            'Motor 3 Current (A)': np.random.normal(12.2, 2, 10),
            'Temperature (°C)': np.random.normal(60, 8, 10),
            'Battery (%)': np.random.normal(75, 10, 10)
        })
        
        st.dataframe(sample_data, use_container_width=True)
    
    # Tab 3: Upload CSV
    with tab3:
        st.markdown("### Upload Telemetry Data")
        
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.success("File uploaded successfully!")
                st.markdown("### Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                st.markdown("---")
                st.markdown("### Data Statistics")
                st.write(df.describe())
            except Exception as e:
                st.error(f"Error reading file: {e}")
        else:
            st.info("Upload a CSV file containing telemetry data to analyze.")
        
        st.markdown("---")
        
        st.markdown("### CSV Format Requirements")
        st.markdown("""
        The CSV file should contain the following columns:
        - Timestamp: Date and time of measurement
        - Motor 1 Current (A): Current for motor 1
        - Motor 2 Current (A): Current for motor 2
        - Motor 3 Current (A): Current for motor 3
        - Temperature (°C): Temperature reading
        - Battery (%): Battery level
        """)
