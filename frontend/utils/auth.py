"""
Authentication Utilities Module

This module provides authentication utilities for managing user sessions,
JWT tokens, and role-based access control.
"""

import streamlit as st
import jwt
from typing import Optional
from datetime import datetime


# JWT configuration (must match backend)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"


def init_session_state() -> None:
    """
    Initialize session state variables for authentication.
    
    This should be called at the start of the app to ensure all
    session state variables are initialized.
    """
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "token" not in st.session_state:
        st.session_state.token = None
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "role" not in st.session_state:
        st.session_state.role = None
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"


def login(username: str, password: str) -> bool:
    """
    Authenticate user and store session information.
    
    Args:
        username: User username
        password: User password
        
    Returns:
        True if login successful, False otherwise
    """
    from utils.api import login as api_login
    
    if api_login(username, password):
        # Decode JWT token to get user information
        try:
            payload = jwt.decode(
                st.session_state.token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            
            st.session_state.user = payload.get("sub")
            st.session_state.user_id = payload.get("user_id")
            st.session_state.role = payload.get("role")
            
            return True
            
        except jwt.PyJWTError:
            st.error("Failed to decode token. Please try again.")
            logout()
            return False
    else:
        return False


def logout() -> None:
    """
    Clear user session and redirect to login.
    """
    from utils.api import logout as api_logout
    
    api_logout()


def is_authenticated() -> bool:
    """
    Check if user is authenticated.
    
    Returns:
        True if user is authenticated, False otherwise
    """
    return st.session_state.get("authenticated", False)


def current_user() -> Optional[str]:
    """
    Get current username.
    
    Returns:
        Current username or None if not authenticated
    """
    return st.session_state.get("user")


def current_role() -> Optional[str]:
    """
    Get current user role.
    
    Returns:
        Current user role or None if not authenticated
    """
    return st.session_state.get("role")


def current_user_id() -> Optional[int]:
    """
    Get current user ID.
    
    Returns:
        Current user ID or None if not authenticated
    """
    return st.session_state.get("user_id")


def is_administrator() -> bool:
    """
    Check if current user is an administrator.
    
    Returns:
        True if user is administrator, False otherwise
    """
    return current_role() == "administrator"


def is_maintenance_engineer() -> bool:
    """
    Check if current user is a maintenance engineer.
    
    Returns:
        True if user is maintenance engineer, False otherwise
    """
    return current_role() == "maintenance_engineer"


def is_drone_operator() -> bool:
    """
    Check if current user is a drone operator.
    
    Returns:
        True if user is drone operator, False otherwise
    """
    return current_role() == "drone_operator"


def require_role(required_role: str) -> bool:
    """
    Check if current user has the required role.
    
    Args:
        required_role: Required role (administrator, maintenance_engineer, drone_operator)
        
    Returns:
        True if user has required role, False otherwise
    """
    return current_role() == required_role


def require_authentication() -> None:
    """
    Require user to be authenticated. Redirect to login if not.
    
    This function should be called at the beginning of any page
    that requires authentication.
    """
    if not is_authenticated():
        st.session_state.current_page = "login"
        st.rerun()


def require_administrator() -> None:
    """
    Require user to be an administrator. Show error if not.
    
    This function should be called at the beginning of any page
    that requires administrator access.
    """
    require_authentication()
    
    if not is_administrator():
        st.error("Access denied. Administrator access required.")
        st.stop()


def get_role_display_name(role: Optional[str]) -> str:
    """
    Get display name for a role.
    
    Args:
        role: Role string (administrator, maintenance_engineer, drone_operator)
        
    Returns:
        Display name for the role
    """
    role_names = {
        "administrator": "Administrator",
        "maintenance_engineer": "Maintenance Engineer",
        "drone_operator": "Drone Operator"
    }
    
    return role_names.get(role, "Unknown")


def get_role_icon(role: Optional[str]) -> str:
    """
    Get icon for a role.
    
    Args:
        role: Role string (administrator, maintenance_engineer, drone_operator)
        
    Returns:
        Icon emoji for the role
    """
    role_icons = {
        "administrator": "👤",
        "maintenance_engineer": "🔧",
        "drone_operator": "🚁"
    }
    
    return role_icons.get(role, "❓")
