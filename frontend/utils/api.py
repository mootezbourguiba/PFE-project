"""
API Client Module

This module provides a reusable API client for communicating with the FastAPI backend.
It handles JWT authentication, error handling, and automatic token management.
"""

import requests
import streamlit as st
from typing import Dict, Any, Optional, List


class APIClient:
    """
    Reusable API client for backend communication.
    
    This class handles:
    - JWT token management
    - Automatic Authorization header injection
    - Error handling (401, 403, 500, connection errors)
    - Request/response logging
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL of the FastAPI backend
        """
        self.base_url = base_url
        self.timeout = 30
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get request headers with JWT token if available.
        
        Returns:
            Dictionary containing headers including Authorization if token exists
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Add JWT token if available in session state
        if "token" in st.session_state and st.session_state.token:
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        
        return headers
    
    def _handle_error(self, response: requests.Response) -> None:
        """
        Handle HTTP errors with appropriate user feedback.
        
        Args:
            response: The failed response object
            
        Raises:
            Streamlit error with user-friendly message
        """
        if response.status_code == 401:
            st.error("Authentication failed. Please log in again.")
            st.session_state.clear()
            st.rerun()
        elif response.status_code == 403:
            st.error("Access denied. You don't have permission for this action.")
        elif response.status_code == 404:
            st.error("Resource not found.")
        elif response.status_code == 500:
            st.error("Server error. Please try again later.")
        elif response.status_code >= 400:
            st.error(f"Request failed with status code {response.status_code}")
    
    def _handle_connection_error(self, error: Exception) -> None:
        """
        Handle connection errors.
        
        Args:
            error: The connection error exception
        """
        st.error("Cannot connect to the backend server. Please ensure it is running.")
        st.error(f"Error: {str(error)}")
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a POST request.
        
        Args:
            endpoint: API endpoint path (e.g., "/api/v1/auth/login")
            data: Request body data
            
        Returns:
            Response JSON data or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.post(
                url,
                json=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                self._handle_error(response)
                return None
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Send a GET request.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response JSON data or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(
                url,
                params=params,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                self._handle_error(response)
                return None
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def put(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a PUT request.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response JSON data or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.put(
                url,
                json=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                self._handle_error(response)
                return None
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def patch(self, endpoint: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a PATCH request.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Response JSON data or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.patch(
                url,
                json=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                self._handle_error(response)
                return None
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def delete(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Send a DELETE request.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Response JSON data or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.delete(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                self._handle_error(response)
                return None
            
            return response.json()
            
        except requests.exceptions.ConnectionError as e:
            self._handle_connection_error(e)
            return None
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            return None


# Global API client instance
api_client = APIClient()


def login(username: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate user with backend.
    
    Args:
        username: User username
        password: User password
        
    Returns:
        Token response dict or None if authentication fails
    """
    # Use form data for OAuth2 password flow
    data = {
        "username": username,
        "password": password
    }
    
    response = api_client.post("/api/v1/auth/login", data)
    
    if response:
        # Store token in session state
        st.session_state.token = response.get("access_token")
        st.session_state.token_type = response.get("token_type")
        return response
    
    return None


def predict_anomaly(current: float, temperature: float) -> Optional[Dict[str, Any]]:
    """
    Predict anomaly from telemetry data.
    
    Args:
        current: Motor current value
        temperature: Motor temperature value
        
    Returns:
        Prediction response dict or None if request fails
    """
    data = {
        "current": current,
        "temperature": temperature
    }
    
    return api_client.post("/api/v1/telemetry/predict", data)


def get_users(skip: int = 0, limit: int = 100) -> Optional[List[Dict[str, Any]]]:
    """
    Get all users (admin only).
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of user dicts or None if request fails
    """
    params = {"skip": skip, "limit": limit}
    response = api_client.get("/api/v1/users/", params)
    
    if response:
        return response
    
    return None


def create_user(username: str, email: str, password: str, role: str) -> Optional[Dict[str, Any]]:
    """
    Create a new user (admin only).
    
    Args:
        username: User username
        email: User email
        password: User password
        role: User role
        
    Returns:
        Created user dict or None if request fails
    """
    data = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    
    return api_client.post("/api/v1/users/", data)


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a specific user by ID (admin only).
    
    Args:
        user_id: User ID
        
    Returns:
        User dict or None if request fails
    """
    return api_client.get(f"/api/v1/users/{user_id}")


def update_user(user_id: int, email: Optional[str] = None, role: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Update a user (admin only).
    
    Args:
        user_id: User ID
        email: New email (optional)
        role: New role (optional)
        
    Returns:
        Updated user dict or None if request fails
    """
    data = {}
    if email:
        data["email"] = email
    if role:
        data["role"] = role
    
    return api_client.put(f"/api/v1/users/{user_id}", data)


def disable_user(user_id: int, disabled: bool, reason: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Disable or enable a user (admin only).
    
    Args:
        user_id: User ID
        disabled: Whether to disable the user
        reason: Reason for disabling (optional)
        
    Returns:
        User status dict or None if request fails
    """
    data = {
        "disabled": disabled,
        "reason": reason
    }
    
    return api_client.patch(f"/api/v1/users/{user_id}/disable", data)


def enable_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Enable a disabled user (admin only).
    
    Args:
        user_id: User ID
        
    Returns:
        User status dict or None if request fails
    """
    return api_client.patch(f"/api/v1/users/{user_id}/enable", {})
