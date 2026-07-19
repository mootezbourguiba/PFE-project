import streamlit as st

st.set_page_config(
    page_title="Avionics Health Monitoring Platform",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ Intelligent Avionics Health Monitoring Platform")

st.markdown("---")

st.subheader("Welcome")

st.write(
    """
This prototype was developed for the Final Year Project (PFE).

Current implementation:

- ✅ Authentication System
- ✅ User Roles
- ✅ Telemetry Simulation
- ✅ Isolation Forest Model
- ✅ REST API
- 🔄 Streamlit Dashboard (under development)
"""
)

st.info("Sprint 4 - Frontend Development")