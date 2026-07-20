"""
AVIONAV Platform - Main Application

This is the main entry point for the AVIONAV Intelligent UAV Health Monitoring Platform.
It handles role-based navigation and routing to different dashboard pages.
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from frontend.utils.auth import init_session_state, is_authenticated, current_role, is_administrator, is_maintenance_engineer, is_drone_operator


def main() -> None:
    """
    Main application function that handles navigation and routing.
    
    This function:
    - Sets page configuration
    - Initializes session state
    - Routes users to appropriate pages based on authentication status and role
    - Handles page navigation
    """
    # Set page configuration (must be first Streamlit command)
    st.set_page_config(
        page_title="AVIONAV Platform",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Custom CSS for dark avionics theme
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d1b2a 0%, #1e3a5f 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Page routing based on authentication and role
    if not is_authenticated():
        # Show login page
        from frontend.pages.login import show as show_login
        show_login()
    else:
        # Get current page from session state
        current_page = st.session_state.get("page", "dashboard")
        
        # Route to appropriate page based on role
        if current_page == "login":
            # Redirect authenticated users to dashboard
            st.session_state.page = "dashboard"
            st.rerun()
        
        elif current_page == "dashboard":
            # Route to role-specific dashboard
            if is_administrator():
                from frontend.pages.dashboard_admin import show as show_admin_dashboard
                show_admin_dashboard()
            elif is_maintenance_engineer():
                from frontend.pages.dashboard_maintenance import show as show_maintenance_dashboard
                show_maintenance_dashboard()
            elif is_drone_operator():
                from frontend.pages.dashboard_operator import show as show_operator_dashboard
                show_operator_dashboard()
            else:
                st.error("Unknown role. Please contact administrator.")
        
        elif current_page == "users":
            # User management page (admin only)
            from frontend.pages.users import show as show_users
            show_users()
        
        elif current_page == "telemetry":
            # Telemetry page
            from frontend.pages.telemetry import show as show_telemetry
            show_telemetry()
        
        elif current_page == "history":
            # History page
            from frontend.pages.history import show as show_history
            show_history()
        
        elif current_page == "settings":
            # Settings page (admin only)
            from frontend.pages.settings import show as show_settings
            show_settings()
        
        else:
            # Default to dashboard
            st.session_state.page = "dashboard"
            st.rerun()


if __name__ == "__main__":
    main()