import streamlit as st

from components.theme import load_css
from components.theme import page_header

st.set_page_config(
    page_title="AVIONAV",
    page_icon="✈️",
    layout="wide",
)

load_css()

page_header(
    "✈️ AVIONAV",
    "Intelligent UAV Health Monitoring Platform",
)

st.write("---")

st.info(
    "Sprint 4 UI is now under construction."
)