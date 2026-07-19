import streamlit as st

from services.auth import authenticate

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 User Login")

st.write("Login to the Avionics Health Monitoring Platform")

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    if authenticate(username, password):

        st.success("Login successful!")

        st.write("JWT stored successfully.")

    else:

        st.error("Invalid username or password.")


        