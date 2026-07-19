import streamlit as st
from services.auth import authenticate

def show():
    """
    Display the login page.
    
    This function is called by the main app navigation system
    when the user is not authenticated.
    """
    st.set_page_config(page_title="Login", page_icon="🔐")

    st.title("🔐 User Login")

    st.write("Login to the Avionics Health Monitoring Platform")

    st.markdown("---")

    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        username = st.text_input("Username", key="login_username")

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):
            if authenticate(username, password):
                st.success("Login successful!")
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # Information about default accounts
    st.markdown("---")
    st.info("""
    **Default Administrator Account:**
    - Username: admin
    - Password: Admin123!
    
    *Note: If the admin account doesn't exist, run the initialization script.*
    """)
        