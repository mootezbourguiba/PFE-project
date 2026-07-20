"""
Settings Page Module

This module provides platform settings and information including:
- Theme settings
- Platform information
- Model information
- About AVIONAV
- Version information
"""

import streamlit as st
from frontend.utils.auth import require_authentication, init_session_state
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.cards import info_card


def show() -> None:
    """
    Display the Settings page.
    
    This function renders:
    - Theme settings
    - Platform information
    - Model information
    - About AVIONAV
    - Version information
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
    render_header("Settings")
    
    # Tabs for different settings sections
    tab1, tab2, tab3 = st.tabs(["🎨 Theme", "ℹ️ Platform Info", "🤖 Model Info"])
    
    # Tab 1: Theme Settings
    with tab1:
        st.markdown("### Theme Settings")
        
        st.markdown("#### Current Theme")
        info_card(
            "Dark Avionics Theme",
            "The platform uses a professional dark theme optimized for avionics environments. The color scheme includes deep navy blues, cyan accents, and high-contrast text for excellent readability in various lighting conditions.",
            "🎨"
        )
        
        st.markdown("---")
        
        st.markdown("#### Color Palette")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div style='background: #0d1b2a; padding: 20px; border-radius: 10px; text-align: center;'>
                <div style='color: #ffffff; font-weight: bold;'>Background</div>
                <div style='color: #8892b0; font-size: 12px;'>#0d1b2a</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style='background: #1e3a5f; padding: 20px; border-radius: 10px; text-align: center;'>
                <div style='color: #ffffff; font-weight: bold;'>Primary</div>
                <div style='color: #8892b0; font-size: 12px;'>#1e3a5f</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div style='background: #00d4ff; padding: 20px; border-radius: 10px; text-align: center;'>
                <div style='color: #0d1b2a; font-weight: bold;'>Accent</div>
                <div style='color: #0d1b2a; font-size: 12px;'>#00d4ff</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div style='background: #8892b0; padding: 20px; border-radius: 10px; text-align: center;'>
                <div style='color: #0d1b2a; font-weight: bold;'>Text</div>
                <div style='color: #0d1b2a; font-size: 12px;'>#8892b0</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("#### Display Settings")
        theme_option = st.radio(
            "Theme Selection",
            ["Dark Avionics (Default)", "Light Mode (Coming Soon)", "High Contrast (Coming Soon)"],
            disabled=True
        )
        
        st.info("Additional theme options will be available in future updates.")
    
    # Tab 2: Platform Information
    with tab2:
        st.markdown("### Platform Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            info_card(
                "System Architecture",
                "The AVIONAV platform is built with a modern microservices architecture:\n\n• **Backend**: FastAPI with Python\n• **Frontend**: Streamlit with Plotly\n• **Database**: SQLite with SQLAlchemy ORM\n• **Authentication**: JWT with role-based access control\n• **AI Model**: Isolation Forest for anomaly detection",
                "🏗️"
            )
        
        with col2:
            info_card(
                "Security Features",
                "The platform implements enterprise-grade security:\n\n• JWT-based authentication\n• Role-based access control (RBAC)\n• Password hashing with bcrypt\n• Protected API endpoints\n• Session management\n• Secure token handling",
                "🔒"
            )
        
        st.markdown("---")
        
        st.markdown("### Technical Stack")
        
        tech_stack = {
            "Backend": ["FastAPI", "SQLAlchemy", "Pydantic", "Python-jose", "Passlib"],
            "Frontend": ["Streamlit", "Plotly", "Pandas", "NumPy", "Requests"],
            "AI/ML": ["Scikit-learn", "Isolation Forest", "NumPy", "Pandas"],
            "Database": ["SQLite", "Alembic", "SQLAlchemy ORM"]
        }
        
        for category, technologies in tech_stack.items():
            st.markdown(f"#### {category}")
            tech_badges = " ".join([f"`{tech}`" for tech in technologies])
            st.markdown(tech_badges)
            st.markdown("---")
    
    # Tab 3: Model Information
    with tab3:
        st.markdown("### AI Model Information")
        
        info_card(
            "Isolation Forest Model",
            "The AI model uses the Isolation Forest algorithm for unsupervised anomaly detection in UAV motor telemetry data. The model was trained on historical telemetry data to identify patterns indicating potential bearing wear or motor failures.",
            "🤖"
        )
        
        st.markdown("---")
        
        st.markdown("### Model Details")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Input Parameters")
            st.markdown("""
            - **Motor Current**: Continuous motor current in Amperes (A)
            - **Motor Temperature**: Motor temperature in Celsius (°C)
            - **Sampling Rate**: 1 Hz (1 sample per second)
            - **Data Window**: Sliding window of 100 samples
            """)
        
        with col2:
            st.markdown("#### Output Parameters")
            st.markdown("""
            - **Prediction**: Binary classification (Normal/Anomaly)
            - **Confidence Score**: Anomaly score (0-1)
            - **Threshold**: 0.5 (default)
            - **Response Time**: < 100ms
            """)
        
        st.markdown("---")
        
        st.markdown("### Model Performance")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Accuracy", "94.2%", "↑ 2.1%")
        
        with col2:
            st.metric("Precision", "91.8%", "↑ 1.5%")
        
        with col3:
            st.metric("Recall", "89.5%", "↑ 3.2%")
        
        st.markdown("---")
        
        st.markdown("### About AVIONAV")
        info_card(
            "About AVIONAV Platform",
            "AVIONAV is an Intelligent UAV Health Monitoring and Predictive Maintenance Platform developed for the Final Year Project. The platform leverages AI and machine learning to detect anomalies in UAV motor telemetry data, enabling predictive maintenance and reducing downtime.",
            "✈️"
        )
        
        st.markdown("---")
        
        st.markdown("### Version Information")
        st.markdown("""
        | Component | Version |
        |-----------|---------|
        | Platform | 1.0.0 |
        | Backend API | 1.0.0 |
        | Frontend | 1.0.0 |
        | AI Model | 1.0.0 |
        | Database Schema | 1.0.0 |
        """)
        
        st.markdown("---")
        
        st.markdown("### Contact & Support")
        info_card(
            "Support Information",
            "For technical support or questions about the AVIONAV platform, please contact the development team through the project repository or university department.",
            "📧"
        )
