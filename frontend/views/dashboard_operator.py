"""
Drone Operator Dashboard

Simplified operational interface for drone operators.
"""

import streamlit as st
import pandas as pd
from components.sidebar import show as render_sidebar
from components.header import show as render_header
from components.cards import kpi_card, info_card, alert_card
from components.charts import line_chart, COLORS
from components.gauges import current_gauge, temperature_gauge
from components.theme import status_badge
from utils.auth import require_drone_operator
from utils.api import get_telemetry_latest, get_telemetry


def _status_color(prediction):
    if prediction == "HEALTHY":
        return COLORS["success"]
    if prediction == "ANOMALY":
        return COLORS["error"]
    return COLORS["text_muted"]


def show() -> None:
    require_drone_operator()
    render_sidebar("dashboard_operator")
    render_header("Operator Dashboard", "UAV motor status and mission overview")

    latest = get_telemetry_latest()

    if not latest or not latest.get("reading"):
        info_card(
            "No Telemetry",
            "Telemetry has not been generated. Contact maintenance for status.",
        )
        st.stop()

    reading = latest.get("reading", {})
    prediction = latest.get("prediction")
    recommendation = latest.get("recommendation") or "No recommendation"

    # Motor status banner
    st.markdown(
        f"""
        <div style="
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        ">
            <div style="color: {COLORS['text_muted']}; font-size: 12px; text-transform: uppercase; font-weight: 600; margin-bottom: 8px;">
                Motor Status
            </div>
            <div style="margin-bottom: 8px;">
                {status_badge(prediction or 'NO DATA')}
            </div>
            <div style="color: {COLORS['white']}; font-size: 16px; font-weight: 600;">
                {recommendation}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if prediction == "ANOMALY":
        alert_card(
            f"Propulsion anomaly detected. Current: {reading.get('current', 'N/A')} A, "
            f"Temperature: {reading.get('temperature', 'N/A')} °C. Inspection required.",
            "error",
        )

    # KPIs
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Mission", "In Progress", "", COLORS["primary"])
    with c2:
        kpi_card("Motor Current", f"{reading.get('current', 0):.2f}", "A", COLORS["accent"])
    with c3:
        kpi_card("Motor Temp", f"{reading.get('temperature', 0):.2f}", "°C", COLORS["warning"])

    # Gauges
    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(
            current_gauge(reading.get("current", 0.0), max_current=50.0),
            use_container_width=True,
        )
    with g2:
        st.plotly_chart(
            temperature_gauge(reading.get("temperature", 0.0), max_temp=100.0),
            use_container_width=True,
        )

    # Live telemetry
    st.markdown(
        """
        <div style="
            color: #FFFFFF;
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin: 24px 0 12px 0;
            border-bottom: 1px solid #1E3A4D;
            padding-bottom: 8px;
        ">Live Telemetry</div>
        """,
        unsafe_allow_html=True,
    )

    telemetry = get_telemetry(limit=50)
    if telemetry and telemetry.get("items"):
        df = pd.DataFrame(telemetry["items"])
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            format="ISO8601",
            utc=True,
        ).dt.tz_localize(None)

        c1, c2 = st.columns(2)
        with c1:
            fig = line_chart(
                df,
                x_col="timestamp",
                y_col="current",
                title="Current (A)",
                color=COLORS["accent"],
                unit="A",
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = line_chart(
                df,
                x_col="timestamp",
                y_col="temperature",
                title="Temperature (°C)",
                color=COLORS["warning"],
                unit="°C",
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        info_card("No Telemetry", "No recent telemetry data available.")
