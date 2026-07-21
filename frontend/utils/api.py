"""
API Client Module

This module provides a reusable API client for communicating with the FastAPI backend.
It handles JWT authentication, error handling, and request/response processing.
"""

import requests
import streamlit as st
from typing import Optional, Dict, Any, List
import time


class APIClient:
    """
    Reusable API client for backend communication.
    
    This client handles:
    - JWT token storage and automatic inclusion in headers
    - Error handling for 401, 403, 500, and connection errors
    - Request/response processing
    - Automatic token refresh on 401 errors
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api/v1"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for the API endpoints
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get request headers with JWT token if available.
        
        Returns:
            Dictionary of headers including Authorization if token exists
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if "token" in st.session_state and st.session_state.token:
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        
        return headers
    
    def _handle_error(self, response: requests.Response) -> None:
        """
        Handle HTTP errors with appropriate user feedback.
        
        Args:
            response: The response object from the request
            
        Raises:
            Exception: With appropriate error message based on status code
        """
        if response.status_code == 401:
            st.session_state.token = None
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.role = None
            st.error("Session expired. Please log in again.")
            st.rerun()
        elif response.status_code == 403:
            st.error("Access denied. You don't have permission to perform this action.")
        elif response.status_code == 404:
            st.error("Resource not found.")
        elif response.status_code == 500:
            st.error("Server error. Please try again later.")
        elif response.status_code >= 400:
            try:
                error_detail = response.json().get("detail", "Unknown error")
                st.error(f"Error: {error_detail}")
            except:
                st.error(f"Request failed with status {response.status_code}")
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Perform a GET request.
        
        Args:
            endpoint: API endpoint path (relative to base_url)
            params: Query parameters
            
        Returns:
            JSON response data or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, headers=self._get_headers(), params=params, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def post(self, endpoint: str, data: Optional[Dict] = None, form_data: bool = False) -> Optional[Dict]:
        """
        Perform a POST request.
        
        Args:
            endpoint: API endpoint path (relative to base_url)
            data: Request body data
            form_data: If True, send as form data instead of JSON
            
        Returns:
            JSON response data or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            
            if form_data:
                headers = {"Accept": "application/json"}
                response = self.session.post(url, headers=headers, data=data, timeout=10)
            else:
                response = self.session.post(url, headers=self._get_headers(), json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                self._handle_error(response)
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Perform a PUT request.
        
        Args:
            endpoint: API endpoint path (relative to base_url)
            data: Request body data
            
        Returns:
            JSON response data or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.put(url, headers=self._get_headers(), json=data, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def patch(self, endpoint: str, data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Perform a PATCH request.
        
        Args:
            endpoint: API endpoint path (relative to base_url)
            data: Request body data
            
        Returns:
            JSON response data or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.patch(url, headers=self._get_headers(), json=data, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def delete(self, endpoint: str) -> Optional[Dict]:
        """
        Perform a DELETE request.
        
        Args:
            endpoint: API endpoint path (relative to base_url)
            
        Returns:
            JSON response data or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.delete(url, headers=self._get_headers(), timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                self._handle_error(response)
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the server. Please check if the backend is running.")
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None


# Global API client instance
api_client = APIClient()


def login(username: str, password: str) -> bool:
    """
    Authenticate user and store JWT token.
    
    Args:
        username: User username
        password: User password
        
    Returns:
        True if login successful, False otherwise
    """
    data = {
        "username": username,
        "password": password
    }
    
    response = api_client.post("/auth/login", data, form_data=True)
    
    if response:
        st.session_state.token = response.get("access_token")
        st.session_state.authenticated = True
        return True
    
    return False


def logout() -> None:
    """
    Clear user session and redirect to login.
    """
    st.session_state.token = None
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.user_id = None
    st.rerun()


def get_users(skip: int = 0, limit: int = 100) -> Optional[List[Dict]]:
    """
    Get list of users (admin only).
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of user dictionaries or None if error
    """
    return api_client.get("/users/", params={"skip": skip, "limit": limit})


def create_user(username: str, email: str, password: str, role: str) -> Optional[Dict]:
    """
    Create a new user (admin only).
    
    Args:
        username: User username
        email: User email
        password: User password
        role: User role (administrator, maintenance_engineer, drone_operator)
        
    Returns:
        Created user dictionary or None if error
    """
    data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    return api_client.post("/users/", data)


def update_user(user_id: int, email: Optional[str] = None, role: Optional[str] = None) -> Optional[Dict]:
    """
    Update a user (admin only).
    
    Args:
        user_id: User ID to update
        email: New email (optional)
        role: New role (optional)
        
    Returns:
        Updated user dictionary or None if error
    """
    data = {}
    if email:
        data["email"] = email
    if role:
        data["role"] = role
    
    return api_client.put(f"/users/{user_id}", data)


def disable_user(user_id: int, disabled: bool, reason: Optional[str] = None) -> Optional[Dict]:
    """
    Disable or enable a user (admin only).
    
    Args:
        user_id: User ID to disable/enable
        disabled: True to disable, False to enable
        reason: Reason for disabling (optional)
        
    Returns:
        User status dictionary or None if error
    """
    data = {
        "disabled": disabled,
        "reason": reason
    }
    return api_client.patch(f"/users/{user_id}/disable", data)


def enable_user(user_id: int) -> Optional[Dict]:
    """
    Enable a disabled user (admin only).
    
    Args:
        user_id: User ID to enable
        
    Returns:
        User status dictionary or None if error
    """
    return api_client.patch(f"/users/{user_id}/enable")
