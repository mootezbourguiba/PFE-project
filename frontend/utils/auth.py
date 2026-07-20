"""
Authentication Utilities Module

This module provides authentication utilities for managing user sessions,
JWT tokens, and role-based access control.
"""

import streamlit as st
import jwt
from datetime import datetime
from typing import Optional, Dict, Any


# JWT configuration (must match backend)
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"


def init_session_state() -> None:
    """
    Initialize session state variables for authentication.
    
    This function ensures all required session state variables are initialized
    to prevent KeyError exceptions during authentication flow.
    """
    if "token" not in st.session_state:
        st.session_state.token = None
    if "token_type" not in st.session_state:
        st.session_state.token_type = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "page" not in st.session_state:
        st.session_state.page = "login"


def login(username: str, password: str) -> bool:
    """
    Authenticate user with backend and store session data.
    
    Args:
        username: User username
        password: User password
        
    Returns:
        True if authentication succeeds, False otherwise
    """
    from frontend.utils.api import login as api_login
    
    # Attempt login via API
    response = api_login(username, password)
    
    if response and "access_token" in response:
        # Decode JWT token to extract user information
        try:
            payload = jwt.decode(
                response["access_token"],
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            
            # Store user information in session state
            st.session_state.token = response["access_token"]
            st.session_state.token_type = response.get("token_type", "bearer")
            st.session_state.user_id = payload.get("user_id")
            st.session_state.username = payload.get("username")
            st.session_state.role = payload.get("role")
            st.session_state.authenticated = True
            
            return True
            
        except jwt.PyJWTError as e:
            st.error(f"Token decoding error: {str(e)}")
            return False
    
    return False


def logout() -> None:
    """
    Log out the current user by clearing session state.
    
    This function removes all authentication-related data from session state
    and redirects to the login page.
    """
    # Clear authentication data
    st.session_state.token = None
    st.session_state.token_type = None
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.authenticated = False
    st.session_state.page = "login"
    
    # Rerun the application to redirect to login
    st.rerun()


def is_authenticated() -> bool:
    """
    Check if the current user is authenticated.
    
    Returns:
        True if user is authenticated, False otherwise
    """
    return st.session_state.get("authenticated", False)


def current_user() -> Optional[Dict[str, Any]]:
    """
    Get information about the current authenticated user.
    
    Returns:
        Dictionary containing user information or None if not authenticated
    """
    if not is_authenticated():
        return None
    
    return {
        "user_id": st.session_state.user_id,
        "username": st.session_state.username,
        "role": st.session_state.role
    }


def current_role() -> Optional[str]:
    """
    Get the role of the current authenticated user.
    
    Returns:
        User role string or None if not authenticated
    """
    return st.session_state.get("role")


def is_administrator() -> bool:
    """
    Check if the current user is an administrator.
    
    Returns:
        True if user is administrator, False otherwise
    """
    return current_role() == "administrator"


def is_maintenance_engineer() -> bool:
    """
    Check if the current user is a maintenance engineer.
    
    Returns:
        True if user is maintenance engineer, False otherwise
    """
    return current_role() == "maintenance_engineer"


def is_drone_operator() -> bool:
    """
    Check if the current user is a drone operator.
    
    Returns:
        True if user is drone operator, False otherwise
    """
    return current_role() == "drone_operator"


def require_authentication() -> None:
    """
    Require authentication for the current page.
    
    If the user is not authenticated, this function displays an error message
    and stops execution. This should be called at the beginning of protected pages.
    """
    if not is_authenticated():
        st.error("Authentication required. Please log in.")
        st.stop()


def require_administrator() -> None:
    """
    Require administrator role for the current page.
    
    If the user is not an administrator, this function displays an error message
    and stops execution. This should be called at the beginning of admin-only pages.
    """
    require_authentication()
    
    if not is_administrator():
        st.error("Administrator access required.")
        st.stop()


def require_maintenance_engineer() -> None:
    """
    Require maintenance engineer role for the current page.
    
    If the user is not a maintenance engineer, this function displays an error message
    and stops execution. This should be called at the beginning of maintenance-only pages.
    """
    require_authentication()
    
    if not is_maintenance_engineer():
        st.error("Maintenance Engineer access required.")
        st.stop()


def require_drone_operator() -> None:
    """
    Require drone operator role for the current page.
    
    If the user is not a drone operator, this function displays an error message
    and stops execution. This should be called at the beginning of operator-only pages.
    """
    require_authentication()
    
    if not is_drone_operator():
        st.error("Drone Operator access required.")
        st.stop()


def get_role_display_name(role: Optional[str]) -> str:
    """
    Get a human-readable display name for a user role.
    
    Args:
        role: Role string (e.g., "administrator")
        
    Returns:
        Human-readable role name
    """
    role_names = {
        "administrator": "Administrator",
        "maintenance_engineer": "Maintenance Engineer",
        "drone_operator": "Drone Operator"
    }
    
    return role_names.get(role, "Unknown")


def get_role_icon(role: Optional[str]) -> str:
    """
    Get an icon for a user role.
    
    Args:
        role: Role string
        
    Returns:
        Emoji icon for the role
    """
    role_icons = {
        "administrator": "👤",
        "maintenance_engineer": "🔧",
        "drone_operator": "🚁"
    }
    
    return role_icons.get(role, "❓")
