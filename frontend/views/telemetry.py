"""
Telemetry Workspace

Professional telemetry simulation and analysis for maintenance engineers.
"""

import pandas as pd
import streamlit as st
from components.sidebar import show as render_sidebar
from components.header import show as render_header
from components.cards import info_card, alert_card, section_title
from components.charts import line_chart, COLORS
from components.gauges import current_gauge, temperature_gauge
from components.theme import status_badge
from utils.auth import require_maintenance_engineer
from utils.api import get_telemetry, simulate_telemetry, upload_telemetry_csv, predict_telemetry


SCENARIO_OPTIONS = {
    "healthy": "Healthy Flight",
    "bearing_wear": "Progressive Bearing Wear",
}


def _to_dataframe(items):
    if not items:
        return pd.DataFrame()
    df = pd.DataFrame(items)
    try:
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True).dt.tz_localize(None)
    except Exception as e:
        st.warning(f"Some telemetry timestamps could not be parsed and were excluded: {e}")
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="ISO8601", utc=True, errors="coerce").dt.tz_localize(None)
        df = df.dropna(subset=["timestamp"]).reset_index(drop=True)
    return df.sort_values("timestamp").reset_index(drop=True)


def show() -> None:
    require_maintenance_engineer()
    render_sidebar("telemetry")
    render_header("Telemetry Workspace", "Simulation, ingestion and analysis")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "● LIVE / LATEST",
        "● HISTORICAL",
        "● SIMULATION",
        "● CSV INGESTION",
        "● AI ANALYSIS",
    ])

    # LIVE / LATEST
    with tab1:
        section_title("Latest Telemetry")
        result = get_telemetry(limit=50)
        if not result or not result.get("items"):
            info_card(
                "No Telemetry Data",
                "Generate a simulated flight or upload a CSV to see telemetry here.",
            )
        else:
            df = _to_dataframe(result["items"])
            latest = df.iloc[-1]

            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(
                    current_gauge(latest["current"], max_current=50.0),
                    use_container_width=True,
                )
            with c2:
                st.plotly_chart(
                    temperature_gauge(latest["temperature"], max_temp=100.0),
                    use_container_width=True,
                )

            c3, c4 = st.columns(2)
            with c3:
                fig = line_chart(
                    df.tail(30),
                    x_col="timestamp",
                    y_col="current",
                    title="Recent Current (A)",
                    color=COLORS["accent"],
                    unit="A",
                    anomaly_col="anomaly",
                )
                st.plotly_chart(fig, use_container_width=True)
            with c4:
                fig = line_chart(
                    df.tail(30),
                    x_col="timestamp",
                    y_col="temperature",
                    title="Recent Temperature (°C)",
                    color=COLORS["warning"],
                    unit="°C",
                    anomaly_col="anomaly",
                )
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(df.tail(20)[["timestamp", "current", "temperature", "anomaly", "source"]], use_container_width=True)

    # HISTORICAL
    with tab2:
        section_title("Historical Telemetry")
        result = get_telemetry(limit=1000)
        if not result or not result.get("items"):
            info_card(
                "No History",
                "Generate or upload telemetry to populate historical records.",
            )
        else:
            df = _to_dataframe(result["items"])

            c1, c2 = st.columns(2)
            with c1:
                fig = line_chart(df, "timestamp", "current", "Current History (A)", color=COLORS["accent"], unit="A", anomaly_col="anomaly")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = line_chart(df, "timestamp", "temperature", "Temperature History (°C)", color=COLORS["warning"], unit="°C", anomaly_col="anomaly")
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                df[["timestamp", "current", "temperature", "anomaly", "source"]],
                use_container_width=True,
            )

    # SIMULATION
    with tab3:
        section_title("Generate Flight Telemetry")
        info_card(
            "Simulation",
            "Generate deterministic, smooth telemetry for healthy flights or progressive bearing-wear scenarios.",
        )

        c1, c2, c3 = st.columns(3)
        with c1:
            scenario = st.selectbox(
                "Scenario",
                options=list(SCENARIO_OPTIONS.keys()),
                format_func=lambda x: SCENARIO_OPTIONS[x],
                key="simulation_scenario_select",
            )
        with c2:
            samples = st.number_input(
                "Readings",
                min_value=10,
                max_value=1000,
                value=100,
                step=10,
                key="simulation_samples_input",
            )
        with c3:
            seed = st.number_input(
                "Seed",
                min_value=0,
                max_value=999999,
                value=42,
                step=1,
                key="simulation_seed_input",
            )

        wear_start = None
        if scenario == "bearing_wear":
            wear_start = st.number_input(
                "Wear start sample",
                min_value=0,
                max_value=int(samples) - 1,
                value=int(samples * 0.3),
                step=1,
                key="simulation_wear_start_input",
            )

        if st.button(
            "GENERATE FLIGHT",
            type="primary",
            key="simulation_generate_button",
            use_container_width=True,
        ):
            with st.spinner("Generating and storing..."):
                res = simulate_telemetry(
                    samples=int(samples),
                    scenario=scenario,
                    wear_start=int(wear_start) if wear_start is not None else None,
                    seed=int(seed),
                )
                if res:
                    st.success(f"Stored {res.get('total', 0)} readings")
                    st.rerun()
                else:
                    alert_card("Failed to generate telemetry", "error")

    # CSV INGESTION
    with tab4:
        section_title("CSV Ingestion")
        info_card(
            "CSV Format",
            "Required columns: timestamp, current (or motor_current), temperature (or motor_temperature). Optional: anomaly.",
        )

        uploaded = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            key="telemetry_csv_uploader",
        )

        if uploaded:
            if st.button(
                "UPLOAD AND STORE",
                type="primary",
                key="csv_upload_store_button",
                use_container_width=True,
            ):
                with st.spinner("Uploading..."):
                    res = upload_telemetry_csv(uploaded)
                    if res:
                        st.success(f"Stored {res.get('total', 0)} readings")
                        df = _to_dataframe(res.get("items", []))
                        st.dataframe(df.head(20), use_container_width=True)
                    else:
                        alert_card("CSV upload failed", "error")

    # AI ANALYSIS
    with tab5:
        section_title("AI Analysis")
        c1, c2, c3 = st.columns(3)
        with c1:
            current_val = st.number_input("Current (A)", min_value=0.01, value=15.0, step=0.1, key="telemetry_ai_current")
        with c2:
            temp_val = st.number_input("Temperature (°C)", min_value=0.01, value=45.0, step=0.1, key="telemetry_ai_temp")
        with c3:
            st.write("")
            st.write("")
            if st.button("ANALYZE", type="primary", key="telemetry_ai_button", use_container_width=True):
                res = predict_telemetry(current_val, temp_val)
                if res:
                    pred = res.get("prediction", "N/A")
                    sc = res.get("score")
                    color = COLORS["success"] if pred == "HEALTHY" else (COLORS["error"] if pred == "ANOMALY" else COLORS["text_muted"])
                    st.markdown(
                        f"""
                        <div style="
                            background: {COLORS['card']};
                            border: 1px solid {color};
                            border-radius: 8px;
                            padding: 20px;
                            margin-top: 12px;
                        ">
                            <div style="color: {COLORS['text_muted']}; font-size: 12px; text-transform: uppercase; font-weight: 600; margin-bottom: 8px;">
                                Prediction
                            </div>
                            <div style="color: {color}; font-size: 26px; font-weight: 700;">{pred}</div>
                            <div style="color: {COLORS['white']}; font-size: 16px; margin-top: 8px;">
                                Anomaly Score: {sc if sc is not None else 'N/A'}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    alert_card("Analysis failed", "error")
