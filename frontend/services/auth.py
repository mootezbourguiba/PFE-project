import jwt
import streamlit as st
from services.api import login

# ===========================
# JWT Configuration
# ===========================
# IMPORTANT: This must match the SECRET_KEY in backend/.env
# For development, use the same key as in .env.example
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"


def authenticate(username: str, password: str) -> bool:
    """
    Authenticate a user with the backend API.
    
    This function:
    1. Sends credentials to the backend login endpoint
    2. Receives JWT token if authentication succeeds
    3. Decodes the token to extract user information
    4. Stores token and user info in session state
    
    Args:
        username: User's username
        password: User's password
        
    Returns:
        True if authentication succeeds, False otherwise
    """
    response = login(username, password)

    if response.status_code != 200:
        return False

    token = response.json()["access_token"]

    # Decode JWT token to extract user information
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    # Store authentication state in session
    st.session_state["token"] = token
    st.session_state["username"] = payload["sub"]
    st.session_state["role"] = payload["role"]
    st.session_state["user_id"] = payload.get("user_id")

    return True