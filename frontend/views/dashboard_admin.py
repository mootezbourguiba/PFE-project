"""
Administrator Dashboard

Operational overview for administrators.
"""

import streamlit as st
import pandas as pd
from components.sidebar import show as render_sidebar
from components.header import show as render_header
from components.cards import kpi_card, info_card, section_title
from components.charts import pie_chart, COLORS
from utils.auth import require_administrator
from utils.api import get_users, get_telemetry_stats


def show() -> None:
    require_administrator()
    render_sidebar("dashboard_admin")
    render_header("Administrator Dashboard", "System overview and user management")

    users = get_users()
    telemetry = get_telemetry_stats()

    users_count = len(users) if users else 0
    total_readings = telemetry.get("total_readings", 0) if telemetry else 0
    anomalous = telemetry.get("anomalous_readings", 0) if telemetry else 0
    healthy = telemetry.get("healthy_readings", 0) if telemetry else 0
    latest_pred = telemetry.get("latest_prediction") if telemetry else None

    # KPIs
    section_title("Platform Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Users", str(users_count), "accounts", COLORS["primary"])
    with c2:
        kpi_card("Telemetry", str(total_readings), "readings", COLORS["accent"])
    with c3:
        kpi_card("Anomalies", str(anomalous), "readings", COLORS["error"])
    with c4:
        pred_text = latest_pred if latest_pred else "N/A"
        pred_color = (
            COLORS["success"] if pred_text == "HEALTHY" else
            (COLORS["error"] if pred_text == "ANOMALY" else COLORS["text_muted"])
        )
        kpi_card("Latest AI", pred_text, "", pred_color)

    # Main content
    c1, c2 = st.columns([1.2, 1])
    with c1:
        section_title("Telemetry Overview")

        overview_data = pd.DataFrame({
            "Category": ["Healthy", "Anomalous", "Unlabeled"],
            "Count": [
                healthy,
                anomalous,
                max(0, total_readings - healthy - anomalous),
            ],
        })

        if total_readings > 0:
            fig = pie_chart(overview_data, "Category", "Count", "Telemetry Status")
            st.plotly_chart(fig, use_container_width=True)
        else:
            info_card("No Telemetry", "No telemetry has been generated yet.")

    with c2:
        section_title("System Status")

        status_items = [
            ("Database", "Connected", COLORS["success"]),
            ("Telemetry Service", "Online" if total_readings is not None else "Idle", COLORS["primary"]),
            ("AI Model", latest_pred if latest_pred else "Idle", COLORS["accent"]),
        ]
        for label, value, color in status_items:
            st.markdown(
                f"""
                <div style="
                    background: {COLORS['card']};
                    border: 1px solid {COLORS['border']};
                    border-radius: 8px;
                    padding: 14px;
                    margin-bottom: 10px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div style="color: {COLORS['text_muted']}; font-size: 13px; font-weight: 600;">{label}</div>
                    <div style="color: {color}; font-weight: 700;">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Quick actions
    section_title("Quick Actions")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("👤  Create User", key="admin_qa_create", use_container_width=True):
            st.session_state.current_page = "users"
            st.rerun()
    with c2:
        if st.button("👥  Manage Users", key="admin_qa_users", use_container_width=True):
            st.session_state.current_page = "users"
            st.rerun()
    with c3:
        if st.button("📡  Telemetry", key="admin_qa_telemetry", use_container_width=True):
            st.warning("Navigation available for maintenance role.")
    with c4:
        if st.button("⚙  Settings", key="admin_qa_settings", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()

    # User list preview
    section_title("User Accounts")
    if users:
        df = pd.DataFrame(users)
        columns = ["username", "email", "role"]
        if "disabled" in df.columns:
            columns.append("disabled")
        df = df[columns].copy()
        df["role"] = df["role"].str.replace("_", " ").str.title()
        if "disabled" in df.columns:
            df["status"] = df["disabled"].apply(lambda x: "Disabled" if x else "Active")
        else:
            df["status"] = "Active"
        st.dataframe(df[["username", "email", "role", "status"]], use_container_width=True)
    else:
        info_card("No Users", "No user data available from the backend.")
