"""
Maintenance Engineer Dashboard

UAV propulsion health monitoring dashboard.
"""

import streamlit as st
import pandas as pd
from components.sidebar import show as render_sidebar
from components.header import show as render_header
from components.cards import kpi_card, info_card, alert_card, section_title
from components.charts import line_chart, COLORS
from components.gauges import current_gauge, temperature_gauge
from components.theme import status_badge
from utils.auth import require_maintenance_engineer
from utils.api import get_telemetry_latest, get_telemetry, predict_telemetry


def _format_score(score):
    if score is None:
        return "N/A"
    return f"{score:.4f}"


def _status_color(prediction):
    if prediction == "HEALTHY":
        return COLORS["success"]
    if prediction == "ANOMALY":
        return COLORS["error"]
    return COLORS["text_muted"]


def _recommendation(prediction):
    if prediction == "HEALTHY":
        return "Normal operation"
    if prediction == "ANOMALY":
        return "Maintenance inspection recommended"
    return "No telemetry available"


def show() -> None:
    require_maintenance_engineer()
    render_sidebar("dashboard_maintenance")
    render_header(
        "Maintenance Dashboard",
        "UAV propulsion health monitoring and predictive maintenance",
    )

    latest = get_telemetry_latest()

    if not latest or not latest.get("reading"):
        section_title("UAV Motor Health")
        info_card(
            "No Telemetry Available",
            "Generate a test flight to begin motor health monitoring.",
        )
        if st.button("🚀  Generate Test Flight", key="dash_maint_gen_flight"):
            st.session_state.current_page = "telemetry"
            st.rerun()
        st.stop()

    reading = latest.get("reading", {})
    prediction = latest.get("prediction")
    score = latest.get("score")
    recommendation = latest.get("recommendation") or _recommendation(prediction)

    # Top health banner
    section_title("UAV Motor Health")
    status_color = _status_color(prediction)
    status_label = prediction if prediction else "NO DATA"

    st.markdown(
        f"""
        <div style="
            background: {COLORS['card']};
            border: 1px solid {status_color};
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        ">
            <div>
                <div style="color: {COLORS['text_muted']}; font-size: 12px; text-transform: uppercase; letter-spacing: 0.6px; font-weight: 600;">
                    Current Status
                </div>
                <div style="color: {status_color}; font-size: 28px; font-weight: 700; margin-top: 4px;">
                    {status_label}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="color: {COLORS['text_muted']}; font-size: 12px; text-transform: uppercase; letter-spacing: 0.6px;">
                    Recommendation
                </div>
                <div style="color: {COLORS['white']}; font-size: 16px; font-weight: 600; margin-top: 4px;">
                    {recommendation}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card(
            "Motor Current",
            f"{reading.get('current', 0):.2f}",
            "A",
            COLORS["accent"],
        )
    with c2:
        kpi_card(
            "Motor Temperature",
            f"{reading.get('temperature', 0):.2f}",
            "°C",
            COLORS["warning"],
        )
    with c3:
        kpi_card(
            "Anomaly Score",
            _format_score(score),
            "Isolation Forest",
            _status_color(prediction),
        )
    with c4:
        kpi_card(
            "System Status",
            "Operational",
            "",
            COLORS["success"],
        )

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

    # Telemetry charts
    section_title("Telemetry Trends")
    telemetry = get_telemetry(limit=100)
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
                title="Motor Current (A)",
                color=COLORS["accent"],
                unit="A",
                anomaly_col="anomaly",
            )
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            fig = line_chart(
                df,
                x_col="timestamp",
                y_col="temperature",
                title="Motor Temperature (°C)",
                color=COLORS["warning"],
                unit="°C",
                anomaly_col="anomaly",
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        info_card("No Telemetry", "Telemetry has not been generated or uploaded yet.")

    # AI Analysis
    section_title("AI Analysis")
    c1, c2 = st.columns([1, 2])
    with c1:
        card_html = f'<div style="background:{COLORS["card"]};border:1px solid {COLORS["border"]};border-radius:8px;padding:20px;"><div style="color:{COLORS["text_muted"]};font-size:12px;text-transform:uppercase;font-weight:600;margin-bottom:12px;">Latest Prediction</div><div style="margin-bottom:12px;">{status_badge(prediction or "NO DATA")}</div><div style="color:{COLORS["text_muted"]};font-size:12px;text-transform:uppercase;font-weight:600;margin:16px 0 8px 0;">Anomaly Score</div><div style="color:{COLORS["white"]};font-size:22px;font-weight:700;">{_format_score(score)}</div><div style="color:{COLORS["text_muted"]};font-size:12px;text-transform:uppercase;font-weight:600;margin:16px 0 8px 0;">Recommendation</div><div style="color:{COLORS["white"]};font-weight:500;">{recommendation}</div></div>'
        st.markdown(card_html, unsafe_allow_html=True)

    with c2:
        c3, c4, c5 = st.columns(3)
        with c3:
            current_input = st.number_input(
                "Current (A)",
                min_value=0.01,
                max_value=50.0,
                value=15.0,
                step=0.1,
                key="dash_maint_current_input",
            )
        with c4:
            temp_input = st.number_input(
                "Temp (°C)",
                min_value=0.01,
                max_value=150.0,
                value=45.0,
                step=0.1,
                key="dash_maint_temp_input",
            )
        with c5:
            st.write("")
            st.write("")
            if st.button(
                "Run Prediction",
                type="primary",
                key="dash_maint_run_pred",
                use_container_width=True,
            ):
                result = predict_telemetry(current_input, temp_input)
                if result:
                    pred = result.get("prediction", "N/A")
                    sc = result.get("score")
                    rec = _recommendation(pred)
                    color = _status_color(pred)
                    st.markdown(
                        f"""
                        <div style="
                            background: {COLORS['card']};
                            border-left: 4px solid {color};
                            border-radius: 8px;
                            padding: 16px;
                            margin-top: 12px;
                        ">
                            <div style="color: {color}; font-weight: 700;">{pred}</div>
                            <div style="color: {COLORS['text']}; font-size: 13px;">Score: {_format_score(sc)}</div>
                            <div style="color: {COLORS['text_muted']}; font-size: 12px; margin-top: 4px;">{rec}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    alert_card("Failed to get prediction", "error")

    # Recent alerts
    section_title("Recent Alerts")
    if telemetry and telemetry.get("items"):
        df = pd.DataFrame(telemetry["items"])
        anomalies = df[df["anomaly"] == True].tail(5)
        if not anomalies.empty:
            for _, row in anomalies.iterrows():
                alert_card(
                    f"{row['timestamp']} | Current: {row['current']} A | Temperature: {row['temperature']} °C",
                    "error",
                )
        else:
            alert_card("No anomalies detected in recent telemetry", "success")
    else:
        alert_card("No telemetry available for alert monitoring", "info")
