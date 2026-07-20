"""
Login Page Module

This module provides a professional login page with beautiful UI and authentication.
"""

import streamlit as st
from frontend.utils.auth import login, init_session_state


def show() -> None:
    """
    Display the professional login page.
    
    This function renders a beautiful login interface with:
    - Background banner
    - Logo and branding
    - Login form with validation
    - Loading spinner during authentication
    - Error handling
    - Automatic redirect on success
    """
    # Initialize session state
    init_session_state()
    
    # Page configuration is handled in app.py
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1e3a5f 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main login container
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px;'>
        <h1 style='color: #00d4ff; font-size: 48px; margin: 0;'>AVIONAV</h1>
        <p style='color: #8892b0; font-size: 18px; margin: 10px 0 30px 0;'>
            Intelligent UAV Health Monitoring<br/>& Predictive Maintenance Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
                   padding: 30px; border-radius: 20px; border: 1px solid #00d4ff;
                   box-shadow: 0 8px 32px rgba(0, 212, 255, 0.2);'>
            <h2 style='color: #ffffff; margin: 0 0 20px 0;'>🔐 Login</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
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
            
            submit_button = st.form_submit_button(
                "Login",
                use_container_width=True,
                type="primary"
            )
            
            if submit_button:
                if not username or not password:
                    st.error("Please enter both username and password.")
                else:
                    # Show loading spinner
                    with st.spinner("Authenticating..."):
                        # Attempt login
                        if login(username, password):
                            st.success("Login successful! Redirecting...")
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Default credentials information
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
               padding: 20px; border-radius: 15px; border-left: 4px solid #ff9800;'>
        <h3 style='color: #ff9800; margin: 0 0 10px 0;'>📋 Default Administrator Account</h3>
        <p style='color: #8892b0; margin: 5px 0;'>
            <strong>Username:</strong> admin<br/>
            <strong>Password:</strong> Admin123!
        </p>
        <p style='color: #8892b0; font-size: 12px; margin: 10px 0 0 0;'>
            * Use this account to access the Administrator dashboard.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #8892b0; font-size: 12px;'>
        © 2026 AVIONAV - Intelligent UAV Health Monitoring Platform
    </div>
    """, unsafe_allow_html=True)
        