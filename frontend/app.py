import streamlit as st

from components.theme import apply_theme
from utils.auth import (
    init_session_state,
    is_authenticated,
    current_role,
)

# ------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------

st.set_page_config(
    page_title="AVIONAV Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# INITIALIZE SESSION
# ------------------------------------------------------------

init_session_state()

# ------------------------------------------------------------
# GLOBAL THEME
# ------------------------------------------------------------

apply_theme()

# Hide sidebar before authentication
if not is_authenticated():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ------------------------------------------------------------
# IMPORT VIEWS
# ------------------------------------------------------------

from views import login
from views import dashboard_admin
from views import dashboard_maintenance
from views import dashboard_operator
from views import users
from views import telemetry
from views import history
from views import settings

# ------------------------------------------------------------
# ROUTER
# ------------------------------------------------------------

if is_authenticated():

    role = current_role()
    current_page = st.session_state.get("current_page")

    # Route based on current page
    if current_page == "dashboard_admin" and role == "administrator":
        dashboard_admin.show()
        st.stop()
    elif current_page == "users" and role == "administrator":
        users.show()
        st.stop()
    elif current_page == "dashboard_maintenance" and role == "maintenance_engineer":
        dashboard_maintenance.show()
        st.stop()
    elif current_page == "telemetry" and role == "maintenance_engineer":
        telemetry.show()
        st.stop()
    elif current_page == "dashboard_operator" and role == "drone_operator":
        dashboard_operator.show()
        st.stop()
    elif current_page == "history" and role == "maintenance_engineer":
        history.show()
        st.stop()
    elif current_page == "settings" and role in ["administrator", "maintenance_engineer"]:
        settings.show()
        st.stop()

    # Default routing based on role
    if role == "administrator":
        dashboard_admin.show()
        st.stop()

    elif role == "maintenance_engineer":
        dashboard_maintenance.show()
        st.stop()

    elif role == "drone_operator":
        dashboard_operator.show()
        st.stop()

# ------------------------------------------------------------
# LOGIN PAGE (Shown when not authenticated)
# ------------------------------------------------------------

login.show()
