"""
Charts Component

Professional Plotly charts with the AVIONAV dark aviation theme.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Optional
from components.theme import COLORS


def _apply_avionav_layout(fig: go.Figure, title: str, height: int = 360) -> go.Figure:
    """Apply the shared AVIONAV dark layout."""
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=COLORS["white"])),
        xaxis=dict(
            gridcolor="rgba(184, 199, 217, 0.08)",
            zerolinecolor="rgba(184, 199, 217, 0.15)",
            tickfont=dict(color=COLORS["text_muted"], size=11),
        ),
        yaxis=dict(
            gridcolor="rgba(184, 199, 217, 0.08)",
            zerolinecolor="rgba(184, 199, 217, 0.15)",
            tickfont=dict(color=COLORS["text_muted"], size=11),
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"], family="Segoe UI, sans-serif"),
        margin=dict(l=45, r=25, t=45, b=40),
        height=height,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLORS["text"]),
        ),
    )
    return fig


def line_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    color: str = COLORS["primary"],
    unit: str = "",
    anomaly_col: str = None,
) -> go.Figure:
    """
    Professional dark line chart with optional anomaly markers.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode="lines",
        name=y_col,
        line=dict(color=color, width=2),
        hovertemplate=f"{y_col}: %{{y:.2f}} {unit}<br>Time: %{{x|%Y-%m-%d %H:%M:%S}}<extra></extra>",
    ))

    if anomaly_col and anomaly_col in data.columns:
        anomalies = data[data[anomaly_col] == True]
        if not anomalies.empty:
            fig.add_trace(go.Scatter(
                x=anomalies[x_col],
                y=anomalies[y_col],
                mode="markers",
                name="Anomaly",
                marker=dict(color=COLORS["error"], size=8, symbol="diamond"),
                hovertemplate=f"{y_col}: %{{y:.2f}} {unit}<br>ANOMALY<extra></extra>",
            ))

    fig = _apply_avionav_layout(fig, title)
    return fig


def multi_line_chart(
    data: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    title: str,
    colors: Optional[List[str]] = None,
    height: int = 360,
) -> go.Figure:
    """Multi-line dark chart."""
    if colors is None:
        colors = [COLORS["primary"], COLORS["warning"], COLORS["accent"]]

    fig = go.Figure()
    for i, y_col in enumerate(y_cols):
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode="lines",
            name=y_col,
            line=dict(color=colors[i % len(colors)], width=2),
        ))

    fig = _apply_avionav_layout(fig, title, height)
    return fig


def pie_chart(
    data: pd.DataFrame,
    labels_col: str,
    values_col: str,
    title: str,
) -> go.Figure:
    """Professional dark pie chart."""
    colors = [COLORS["primary"], COLORS["accent"], COLORS["warning"], COLORS["error"]]

    fig = go.Figure(data=[go.Pie(
        labels=data[labels_col],
        values=data[values_col],
        marker=dict(colors=colors[:len(data)]),
        textinfo="label+percent",
        textfont=dict(color=COLORS["white"], size=12),
        hovertemplate="%{label}<br>%{value}<extra></extra>",
    )])

    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=COLORS["white"])),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text"]),
        margin=dict(l=25, r=25, t=45, b=25),
        height=340,
        showlegend=False,
    )
    return fig


def bar_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    color: str = COLORS["primary"],
) -> go.Figure:
    """Professional dark bar chart."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data[x_col],
        y=data[y_col],
        marker=dict(color=color, line=dict(color=color, width=1.5)),
        text=data[y_col],
        textposition="outside",
        textfont=dict(color=COLORS["white"], size=11),
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))

    fig = _apply_avionav_layout(fig, title)
    return fig


def scatter_chart(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    title: str,
    color_col: Optional[str] = None,
) -> go.Figure:
    """Professional dark scatter chart."""
    if color_col:
        fig = px.scatter(
            data,
            x=x_col,
            y=y_col,
            color=color_col,
            title=title,
            color_discrete_sequence=[COLORS["primary"], COLORS["warning"], COLORS["error"]],
        )
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode="markers",
            marker=dict(color=COLORS["primary"], size=8),
        ))

    fig = _apply_avionav_layout(fig, title)
    return fig
