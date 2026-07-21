"""
Login Page

This module provides a professional login page for the AVIONAV platform.
"""

import streamlit as st
from utils.auth import login, init_session_state


def show() -> None:
    """
    Display the professional login page with dark avionics theme.
    """
    # Initialize session state
    init_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="AVIONAV - Login",
        page_icon="✈",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0D1B2A 0%, #1E3A5F 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Logo and Brand
    st.markdown("""
    <div style='text-align: center; padding: 40px 0;'>
        <h1 style='color: #00D4FF; font-size: 48px; margin: 0;'>✈ AVIONAV</h1>
        <p style='color: #B0B0B0; font-size: 18px; margin: 10px 0;'>Intelligent UAV Health Monitoring & Predictive Maintenance Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
                   padding: 30px; border-radius: 20px; border: 2px solid #00D4FF; 
                   box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);'>
            <h2 style='color: #FFFFFF; text-align: center; margin: 0 0 20px 0;'>🔐 Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        remember_me = st.checkbox("Remember me", key="login_remember")
        
        login_button = st.button(
            "Login",
            use_container_width=True,
            type="primary",
            key="login_button"
        )
        
        if login_button:
            if username and password:
                with st.spinner("Authenticating..."):
                    if login(username, password):
                        st.success("Login successful! Redirecting...")
                        
                        # Redirect based on role
                        from utils.auth import current_role
                        role = current_role()
                        
                        if role == "administrator":
                            st.session_state.current_page = "dashboard_admin"
                        elif role == "maintenance_engineer":
                            st.session_state.current_page = "dashboard_maintenance"
                        elif role == "drone_operator":
                            st.session_state.current_page = "dashboard_operator"
                        else:
                            st.session_state.current_page = "dashboard_admin"
                        
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")
            else:
                st.warning("Please enter both username and password.")
    
    st.markdown("---")
    
    # Default credentials information
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px; border-radius: 15px; border-left: 4px solid #00D4FF;'>
        <h3 style='color: #00D4FF; font-size: 16px; margin: 0 0 10px 0;'>📋 Default Administrator Account</h3>
        <p style='color: #B0B0B0; font-size: 14px; margin: 5px 0;'>
            <strong>Username:</strong> admin<br>
            <strong>Password:</strong> Admin123!
        </p>
        <p style='color: #808080; font-size: 12px; margin: 10px 0 0 0;'>
            * Use this account to access the platform for the first time.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <p style='color: #606060; font-size: 12px; margin: 0;'>Version 1.0.0</p>
        <p style='color: #404040; font-size: 10px; margin: 5px 0;'>© 2026 AVIONAV - Intelligent UAV Health Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
        