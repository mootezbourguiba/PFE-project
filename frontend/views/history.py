"""
History Page

Persisted telemetry and on-demand AI analysis.
"""

import streamlit as st
import pandas as pd
from components.sidebar import show as render_sidebar
from components.header import show as render_header
from components.cards import info_card, alert_card, section_title
from components.charts import line_chart, COLORS
from components.theme import status_badge
from utils.auth import require_maintenance_engineer
from utils.api import get_telemetry, predict_telemetry


def _load_telemetry():
    result = get_telemetry(limit=1000)
    if not result or not result.get("items"):
        return pd.DataFrame()
    df = pd.DataFrame(result["items"])
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        format="ISO8601",
        utc=True,
    ).dt.tz_localize(None)
    return df.sort_values("timestamp").reset_index(drop=True)


def show() -> None:
    require_maintenance_engineer()
    render_sidebar("history")
    render_header("History", "Telemetry records and AI analysis")

    df = _load_telemetry()

    tab1, tab2, tab3 = st.tabs(["● TELEMETRY HISTORY", "● AI ANALYSIS", "● ALERTS"])

    with tab1:
        section_title("Telemetry History")

        if df.empty:
            info_card(
                "No Historical Telemetry",
                "Generate a simulation or upload a CSV to populate history.",
            )
        else:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=df["timestamp"].min().date(),
                    key="hist_start_date",
                )
            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=df["timestamp"].max().date(),
                    key="hist_end_date",
                )

            mask = (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
            filtered = df.loc[mask].copy()

            c1, c2 = st.columns(2)
            with c1:
                fig = line_chart(
                    filtered,
                    "timestamp",
                    "current",
                    "Current (A)",
                    color=COLORS["accent"],
                    unit="A",
                    anomaly_col="anomaly",
                )
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig = line_chart(
                    filtered,
                    "timestamp",
                    "temperature",
                    "Temperature (°C)",
                    color=COLORS["warning"],
                    unit="°C",
                    anomaly_col="anomaly",
                )
                st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                filtered[["timestamp", "current", "temperature", "anomaly", "source"]],
                use_container_width=True,
            )

            if not filtered.empty:
                csv = filtered[["timestamp", "current", "temperature", "anomaly", "source"]].to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="telemetry_history.csv",
                    mime="text/csv",
                    key="hist_download_csv",
                )

    with tab2:
        section_title("AI Analysis on Historical Telemetry")

        if df.empty:
            info_card("No Data", "There is no telemetry to analyze.")
        else:
            sample_size = st.slider(
                "Readings to analyze",
                min_value=5,
                max_value=min(100, len(df)),
                value=min(20, len(df)),
                key="hist_analysis_sample_size",
            )

            if st.button(
                "RUN AI ANALYSIS",
                type="primary",
                key="hist_run_analysis",
                use_container_width=True,
            ):
                with st.spinner("Running predictions..."):
                    analysis = []
                    for _, row in df.tail(sample_size).iterrows():
                        result = predict_telemetry(row["current"], row["temperature"])
                        pred = result.get("prediction", "N/A") if result else "N/A"
                        sc = result.get("score") if result else None
                        analysis.append({
                            "timestamp": row["timestamp"],
                            "current": row["current"],
                            "temperature": row["temperature"],
                            "prediction": pred,
                            "score": sc if sc is not None else "N/A",
                        })

                    results_df = pd.DataFrame(analysis)
                    st.dataframe(results_df, use_container_width=True)

                    anomaly_count = (results_df["prediction"] == "ANOMALY").sum()
                    if anomaly_count > 0:
                        alert_card(f"{anomaly_count} anomalies detected in the analyzed sample.", "error")
                    else:
                        alert_card("No anomalies in the analyzed sample.", "success")

    with tab3:
        section_title("Alert History")

        if df.empty:
            info_card("No Alerts", "No telemetry available.")
        else:
            anomalies = df[df["anomaly"] == True]
            if anomalies.empty:
                alert_card("No anomalous telemetry readings recorded.", "success")
            else:
                for _, row in anomalies.tail(10).iterrows():
                    alert_card(
                        f"{row['timestamp']} | Current: {row['current']} A | Temp: {row['temperature']} °C",
                        "error",
                    )
