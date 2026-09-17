import sys
sys.path.insert(0, 'frontend')
import streamlit as st

captured = []
st.markdown = lambda *a, **k: captured.append((a, k))

from components.cards import info_card

# The exact content string now on disk in views/settings.py lines 84-88
content = (
    "Pre-trained model for anomaly detection in UAV propulsion systems.<br>"
    "- Algorithm: Isolation Forest<br>"
    "- Features: Motor Current (A), Motor Temperature (°C)<br>"
    "- Purpose: Bearing-wear and anomaly detection<br>"
    "- Output: HEALTHY or ANOMALY + anomaly score"
)
info_card("Isolation Forest", content)
md = captured[0][0][0]
print("=== EMITTED MARKDOWN ===")
print(md)
print("=== CHECKS ===")
print("blank lines inside block:", any(line.strip() == "" for line in md.strip().splitlines()))
print("unsafe_allow_html:", captured[0][1].get("unsafe_allow_html"))
