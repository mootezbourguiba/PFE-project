"""
Cards Component

Professional AVIONAV cards for metrics, status, info and alerts.
"""

import streamlit as st
from components.theme import COLORS


def _card_base(padding: int = 16, border_left: str = None):
    """Return common card CSS opening."""
    border = f"border-left: 4px solid {border_left};" if border_left else ""
    return f"""
    <div style="
        background: {COLORS['card']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: {padding}px;
        {border}
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    ">
    """


def kpi_card(label: str, value: str, unit: str = "", status_color: str = None) -> None:
    """
    Compact professional KPI card.
    """
    color = status_color or COLORS["primary"]
    unit_html = (
        f'<div style="color: {COLORS["text"]}; font-size: 12px; margin-top: 4px;">{unit}</div>'
        if unit else ""
    )
    st.markdown(
        f"""
        <div style="
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 18px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            border-top: 3px solid {color};
        ">
            <div style="
                color: {COLORS['text_muted']};
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                font-weight: 600;
                margin-bottom: 8px;
            ">{label}</div>
            <div style="
                color: {COLORS['white']};
                font-size: 28px;
                font-weight: 700;
                line-height: 1.1;
            ">{value}</div>
            {unit_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon: str, label: str, value: str, color: str = None) -> None:
    """Legacy metric card — kept for compatibility."""
    kpi_card(label, value, unit="", status_color=color or COLORS["primary"])


def status_card(label: str, status: str, color: str = None) -> None:
    """Display a status card with colored border and text."""
    border_color = color or COLORS["primary"]
    st.markdown(
        f"""
        <div style="
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 16px;
            border-left: 4px solid {border_color};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        ">
            <div style="
                color: {COLORS['text_muted']};
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-weight: 600;
                margin-bottom: 6px;
            ">{label}</div>
            <div style="
                color: {color or COLORS['white']};
                font-size: 18px;
                font-weight: 700;
            ">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """Display an info card."""
    st.markdown(
        f"""
        <div style="
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 20px;
            border-left: 4px solid {COLORS['primary']};
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        ">
            <div style="
                color: {COLORS['white']};
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 8px;
            ">{icon} {title}</div>
            <div style="
                color: {COLORS['text']};
                font-size: 14px;
                line-height: 1.6;
            ">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert_card(message: str, alert_type: str = "warning") -> None:
    """Display an alert card with appropriate status color."""
    colors = {
        "warning": (COLORS["warning"], "⚠ WARNING"),
        "error": (COLORS["error"], "⚠ ERROR"),
        "success": (COLORS["success"], "✓ SUCCESS"),
        "info": (COLORS["info"], "ℹ INFO"),
    }
    color, label = colors.get(alert_type, (COLORS["warning"], alert_type.upper()))
    st.markdown(
        f"""
        <div style="
            background: {COLORS['card']};
            border: 1px solid {color};
            border-radius: 8px;
            padding: 14px 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            margin-bottom: 10px;
        ">
            <div style="
                color: {color};
                font-weight: 700;
                font-size: 12px;
                letter-spacing: 0.4px;
                margin-bottom: 4px;
            ">{label}</div>
            <div style="color: {COLORS['text']}; font-size: 14px;">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str) -> None:
    """Display a professional section title."""
    st.markdown(
        f"""
        <div style="
            color: {COLORS['white']};
            font-size: 16px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            margin: 24px 0 12px 0;
            border-bottom: 1px solid {COLORS['border']};
            padding-bottom: 8px;
        ">{text}</div>
        """,
        unsafe_allow_html=True,
    )


def action_button(label: str, page: str) -> None:
    """Display a quick-action card that navigates to another page."""
    if st.button(label, key=f"quick_action_{page}", use_container_width=True):
        st.session_state.current_page = page
        st.rerun()
