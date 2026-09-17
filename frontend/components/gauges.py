"""
Gauges Component

Professional engineering gauges for AVIONAV.
"""

import plotly.graph_objects as go
from components.theme import COLORS


def _gauge(
    value: float,
    title: str,
    min_val: float,
    max_val: float,
    unit: str,
    color: str,
    steps: list,
) -> go.Figure:
    """Base gauge builder."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": title,
            "font": {"size": 15, "color": COLORS["white"]},
        },
        number={
            "font": {"size": 30, "color": COLORS["white"], "family": "Segoe UI"},
            "suffix": f" {unit}" if unit else "",
        },
        gauge={
            "axis": {
                "range": [min_val, max_val],
                "tickwidth": 1,
                "tickcolor": COLORS["text_muted"],
            },
            "bar": {"color": color, "thickness": 0.7},
            "bgcolor": COLORS["surface"],
            "borderwidth": 1,
            "bordercolor": COLORS["border"],
            "steps": steps,
            "threshold": {
                "line": {"color": COLORS["white"], "width": 3},
                "thickness": 0.8,
                "value": value,
            },
        },
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], family="Segoe UI"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250,
    )
    return fig


def current_gauge(current: float, max_current: float = 50.0) -> go.Figure:
    """Professional current gauge."""
    ratio = current / max_current if max_current else 0
    if ratio < 0.7:
        color = COLORS["accent"]
    elif ratio < 0.9:
        color = COLORS["warning"]
    else:
        color = COLORS["error"]

    steps = [
        {"range": [0, max_current * 0.7], "color": "rgba(0, 255, 204, 0.12)"},
        {"range": [max_current * 0.7, max_current * 0.9], "color": "rgba(255, 145, 0, 0.12)"},
        {"range": [max_current * 0.9, max_current], "color": "rgba(255, 68, 68, 0.12)"},
    ]

    return _gauge(current, "CURRENT", 0, max_current, "A", color, steps)


def temperature_gauge(temperature: float, max_temp: float = 100.0) -> go.Figure:
    """Professional temperature gauge."""
    ratio = temperature / max_temp if max_temp else 0
    if ratio < 0.5:
        color = COLORS["primary"]
    elif ratio < 0.75:
        color = COLORS["warning"]
    else:
        color = COLORS["error"]

    steps = [
        {"range": [0, max_temp * 0.5], "color": "rgba(0, 194, 255, 0.12)"},
        {"range": [max_temp * 0.5, max_temp * 0.75], "color": "rgba(255, 145, 0, 0.12)"},
        {"range": [max_temp * 0.75, max_temp], "color": "rgba(255, 68, 68, 0.12)"},
    ]

    return _gauge(temperature, "TEMPERATURE", 0, max_temp, "°C", color, steps)


def health_gauge(health_score: float) -> go.Figure:
    """
    Health score gauge (0-100).
    Kept for compatibility but score should be passed as a real value.
    """
    if health_score >= 80:
        color = COLORS["success"]
    elif health_score >= 50:
        color = COLORS["warning"]
    else:
        color = COLORS["error"]

    steps = [
        {"range": [0, 50], "color": "rgba(255, 68, 68, 0.12)"},
        {"range": [50, 80], "color": "rgba(255, 145, 0, 0.12)"},
        {"range": [80, 100], "color": "rgba(0, 200, 83, 0.12)"},
    ]

    return _gauge(health_score, "HEALTH", 0, 100, "%", color, steps)
