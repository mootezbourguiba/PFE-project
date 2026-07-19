import requests

# ===========================
# FastAPI Backend URL
# ===========================

BASE_URL = "http://127.0.0.1:8000/api/v1"


# ===========================
# Authentication
# ===========================

def login(username: str, password: str):
    """
    Authenticate a user and return the JWT token.
    
    Args:
        username: User's username
        password: User's password
        
    Returns:
        Response object with JWT token in JSON if successful
    """
    url = f"{BASE_URL}/auth/login"

    data = {
        "username": username,
        "password": password,
    }

    response = requests.post(url, data=data)

    return response


# ===========================
# User Management
# ===========================

def get_users(token: str):
    """
    Get list of all users (Administrator only).
    
    Args:
        token: JWT authentication token
        
    Returns:
        Response object with list of users in JSON
    """
    url = f"{BASE_URL}/users/"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(url, headers=headers)
    
    return response


def create_user(username: str, email: str, password: str, role: str, token: str):
    """
    Create a new user (Administrator only).
    
    Args:
        username: New user's username
        email: New user's email
        password: New user's password
        role: New user's role (administrator, maintenance_engineer, drone_operator)
        token: JWT authentication token
        
    Returns:
        Response object with created user data in JSON
    """
    url = f"{BASE_URL}/users/"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    return response


def update_user(user_id: int, token: str, **kwargs):
    """
    Update a user (Administrator only).
    
    Args:
        user_id: ID of user to update
        token: JWT authentication token
        **kwargs: Fields to update (email, role, etc.)
        
    Returns:
        Response object with updated user data in JSON
    """
    url = f"{BASE_URL}/users/{user_id}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.put(url, json=kwargs, headers=headers)
    
    return response


def delete_user(user_id: int, token: str):
    """
    Delete a user (Administrator only).
    
    Args:
        user_id: ID of user to delete
        token: JWT authentication token
        
    Returns:
        Response object confirming deletion
    """
    url = f"{BASE_URL}/users/{user_id}"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.delete(url, headers=headers)
    
    return response


# ===========================
# Telemetry Prediction
# ===========================

def predict(current: float,
            temperature: float,
            token: str):
    """
    Send telemetry to the backend for anomaly detection.
    
    Args:
        current: Motor current in Amperes
        temperature: Motor temperature in Celsius
        token: JWT authentication token
        
    Returns:
        Response object with prediction result
    """
    url = f"{BASE_URL}/telemetry/predict"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "current": current,
        "temperature": temperature,
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
    )

    return response