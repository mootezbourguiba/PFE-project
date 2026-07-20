"""
Telemetry Page Module

This module provides telemetry data visualization and analysis including:
- Live telemetry display
- Historical telemetry
- CSV upload for analysis
- Prediction results
"""

import streamlit as st
import pandas as pd
import numpy as np
from frontend.utils.auth import require_authentication, init_session_state
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import metric_card, info_card
from frontend.components.charts import line_chart, scatter_chart
from frontend.components.gauges import gauge_chart
from frontend.utils.api import predict_anomaly


def show() -> None:
    """
    Display the Telemetry page.
    
    This function renders:
    - Live telemetry display
    - Historical telemetry charts
    - CSV upload for analysis
    - AI prediction results
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
    render_header("Telemetry Data")
    
    # Tabs for different telemetry views
    tab1, tab2, tab3 = st.tabs(["📊 Live Telemetry", "📁 Upload CSV", "🤖 Predictions"])
    
    # Tab 1: Live Telemetry
    with tab1:
        st.markdown("### Live Telemetry Display")
        
        # Simulated live data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            metric_card("Motor Current", "2.45 A", "⚡", "#00d4ff")
        
        with col2:
            metric_card("Motor Temperature", "42.3 °C", "🌡️", "#ff9800")
        
        with col3:
            metric_card("Battery Voltage", "12.4 V", "🔋", "#00ff88")
        
        with col4:
            metric_card("Signal Strength", "85%", "📶", "#9c27b0")
        
        st.markdown("---")
        
        # Live charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Generate sample live data
            time_points = list(range(100))
            current_data = [2.0 + 0.5 * np.sin(i/10) + 0.2 * np.random.randn() for i in time_points]
            line_chart("Motor Current (Live)", time_points, current_data, "Time (s)", "Current (A)", "#00d4ff")
        
        with col2:
            temp_data = [40 + 8 * np.sin(i/10) + 3 * np.random.randn() for i in time_points]
            line_chart("Motor Temperature (Live)", time_points, temp_data, "Time (s)", "Temperature (°C)", "#ff9800")
        
        st.markdown("---")
        
        # Scatter plot for correlation
        st.markdown("### Current vs Temperature Correlation")
        scatter_chart(
            "Motor Current vs Temperature",
            current_data,
            temp_data,
            "Current (A)",
            "Temperature (°C)",
            "#00d4ff"
        )
    
    # Tab 2: Upload CSV
    with tab2:
        st.markdown("### Upload Telemetry CSV")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            help="Upload a CSV file containing telemetry data for analysis"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                
                st.success(f"File uploaded successfully! Shape: {df.shape}")
                
                # Display data preview
                st.markdown("#### Data Preview")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Display data statistics
                st.markdown("#### Data Statistics")
                st.dataframe(df.describe(), use_container_width=True)
                
                # Check for required columns
                if 'current' in df.columns and 'temperature' in df.columns:
                    st.markdown("#### Telemetry Charts")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        line_chart(
                            "Current from CSV",
                            list(range(len(df))),
                            df['current'].tolist(),
                            "Sample",
                            "Current (A)",
                            "#00d4ff"
                        )
                    
                    with col2:
                        line_chart(
                            "Temperature from CSV",
                            list(range(len(df))),
                            df['temperature'].tolist(),
                            "Sample",
                            "Temperature (°C)",
                            "#ff9800"
                        )
                else:
                    st.warning("CSV must contain 'current' and 'temperature' columns for full analysis.")
                    
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
        else:
            info_card(
                "CSV Upload Instructions",
                "Upload a CSV file containing telemetry data. The file should include columns for 'current' and 'temperature' for AI analysis. Other columns will be displayed in the data preview.",
                "📁"
            )
    
    # Tab 3: Predictions
    with tab3:
        st.markdown("### AI Anomaly Prediction")
        
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                pred_current = st.slider(
                    "Motor Current (A)",
                    min_value=0.0,
                    max_value=5.0,
                    value=2.5,
                    step=0.1
                )
            
            with col2:
                pred_temp = st.slider(
                    "Motor Temperature (°C)",
                    min_value=0.0,
                    max_value=100.0,
                    value=45.0,
                    step=1.0
                )
            
            predict_button = st.form_submit_button("Run Prediction", type="primary")
            
            if predict_button:
                result = predict_anomaly(pred_current, pred_temp)
                
                if result:
                    prediction = result.get("prediction", "unknown")
                    score = result.get("score", 0.0)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if prediction == "anomaly":
                            st.markdown("""
                            <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                                       padding: 30px; border-radius: 15px; border: 2px solid #ff4444;
                                       text-align: center;'>
                                <h2 style='color: #ff4444; margin: 0;'>⚠️ Anomaly Detected</h2>
                                <p style='color: #ffffff; font-size: 18px; margin: 10px 0;'>
                                    Confidence Score: {:.2f}
                                </p>
                                <p style='color: #8892b0;'>
                                    Immediate inspection recommended
                                </p>
                            </div>
                            """.format(score), unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                                       padding: 30px; border-radius: 15px; border: 2px solid #00ff88;
                                       text-align: center;'>
                                <h2 style='color: #00ff88; margin: 0;'>✅ Normal Operation</h2>
                                <p style='color: #ffffff; font-size: 18px; margin: 10px 0;'>
                                    Confidence Score: {:.2f}
                                </p>
                                <p style='color: #8892b0;'>
                                    All parameters within normal range
                                </p>
                            </div>
                            """.format(score), unsafe_allow_html=True)
                    
                    with col2:
                        gauge_chart("Input Current", pred_current, 0, 5, "A", "#00d4ff")
                        gauge_chart("Input Temperature", pred_temp, 0, 100, "°C", "#ff9800")
                else:
                    st.error("Failed to get prediction from backend. Please check your connection.")
        
        st.markdown("---")
        
        # Model information
        info_card(
            "AI Model Details",
            "The Isolation Forest model was trained on historical UAV motor telemetry data to detect anomalies indicating potential bearing wear or motor failures. The model analyzes current and temperature patterns to identify deviations from normal operation.",
            "🤖"
        )
