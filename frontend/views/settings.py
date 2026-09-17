"""
Settings Page

Platform and AI model information.
"""

from pathlib import Path
import streamlit as st
from components.sidebar import show as render_sidebar
from components.header import show as render_header
from components.cards import info_card, section_title
from components.theme import COLORS
from utils.auth import require_authentication


def _count_rows(path: Path) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return str(sum(1 for _ in f) - 1)
    except Exception:
        return "N/A"


def show() -> None:
    require_authentication()
    render_sidebar("settings")
    render_header("Settings", "Platform configuration and model information")

    root = Path(__file__).parent.parent.parent
    model_path = root / "backend" / "ml" / "saved_models" / "isolation_forest.pkl"
    healthy_data_path = root / "datasets" / "healthy_flight_data.csv"
    bearing_data_path = root / "datasets" / "bearing_wear_data.csv"

    tab1, tab2, tab3 = st.tabs(["● PLATFORM", "● AI MODEL", "● ABOUT"])

    with tab1:
        section_title("Platform Information")
        st.markdown(
            f"""
            <div style="
                background: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 24px;
                margin-bottom: 20px;
            ">
                <p style="color: {COLORS['white']}; font-size: 18px; font-weight: 700; margin: 0 0 12px 0;">AVIONAV UAV Health Monitoring</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;"><strong>Version:</strong> 1.0.0</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;"><strong>Project:</strong> Final Year Engineering Project</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;"><strong>Academic Year:</strong> 2025-2026</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        section_title("Technology Stack")
        tech = [
            ("Frontend", "Streamlit, Plotly, Requests"),
            ("Backend", "FastAPI, SQLAlchemy, SQLite"),
            ("AI/ML", "Scikit-learn, Isolation Forest"),
            ("Database", "SQLite with Alembic"),
        ]
        for cat, val in tech:
            st.markdown(
                f"""
                <div style="
                    background: {COLORS['card']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 8px;
                    padding: 14px;
                    margin-bottom: 10px;
                ">
                    <span style="color: {COLORS['white']}; font-weight: 600;">{cat}:</span>
                    <span style="color: {COLORS['text']};">{val}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with tab2:
        section_title("AI Model Information")
        info_card(
            "Isolation Forest",
            "Pre-trained model for anomaly detection in UAV propulsion systems.<br>"
            "- Algorithm: Isolation Forest<br>"
            "- Features: Motor Current (A), Motor Temperature (°C)<br>"
            "- Purpose: Bearing-wear and anomaly detection<br>"
            "- Output: HEALTHY or ANOMALY + anomaly score",
        )

        model_exists = model_path.exists()
        model_status = "Loaded" if model_exists else "Not found"
        model_color = COLORS["success"] if model_exists else COLORS["error"]

        st.markdown(
            f'<div style="background:{COLORS["card"]};border:1px solid {COLORS["border"]};border-radius:8px;padding:24px;">'
            f'<p style="color:{COLORS["text"]};margin:6px 0;"><strong>Model file:</strong> {model_path}</p>'
            f'<p style="color:{COLORS["text"]};margin:6px 0;"><strong>Status:</strong> <span style="color:{model_color};">{model_status}</span></p>'
            f'<p style="color:{COLORS["text"]};margin:6px 0;"><strong>Healthy training data:</strong> {_count_rows(healthy_data_path)} samples</p>'
            f'<p style="color:{COLORS["text"]};margin:6px 0;"><strong>Bearing-wear data:</strong> {_count_rows(bearing_data_path)} samples</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.info(
            "Accuracy, precision, recall and F1 are not reported at runtime. "
            "Run `backend/ml/evaluate_model.py` to obtain verified evaluation metrics."
        )

    with tab3:
        section_title("About AVIONAV")
        st.markdown(
            f"""
            <div style="
                background: {COLORS['card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 24px;
            ">
                <p style="color: {COLORS['white']}; font-size: 18px; font-weight: 700; margin: 0 0 10px 0;">AVIONAV Platform</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;">Intelligent UAV Health Monitoring and Predictive Maintenance</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;"><strong>Company:</strong> AVIONAV</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;"><strong>Project:</strong> Final Year Engineering Project</p>
                <p style="color: {COLORS['text']}; margin: 4px 0;"><strong>Academic Year:</strong> 2025-2026</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style="text-align: center; color: #7C8FA3; font-size: 12px; margin-top: 30px;">
                <p>© 2026 AVIONAV. All rights reserved.</p>
                <p>Intelligent UAV Health Monitoring Platform</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
