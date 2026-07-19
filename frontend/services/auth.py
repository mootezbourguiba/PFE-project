import jwt
import streamlit as st

from services.api import login

SECRET_KEY = "YOUR_SECRET_KEY"      # Use the same key as your FastAPI backend
ALGORITHM = "HS256"


def authenticate(username: str, password: str):

    response = login(username, password)

    if response.status_code != 200:
        return False

    token = response.json()["access_token"]

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    st.session_state["token"] = token
    st.session_state["username"] = payload["sub"]
    st.session_state["role"] = payload["role"]

    return True