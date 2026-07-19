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
    """

    url = f"{BASE_URL}/auth/login"

    data = {
        "username": username,
        "password": password,
    }

    response = requests.post(url, data=data)

    return response


# ===========================
# Telemetry Prediction
# ===========================

def predict(current: float,
            temperature: float,
            token: str):
    """
    Send telemetry to the backend.
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