"""
Gauges Component Module

This module provides reusable gauge charts for displaying metrics with ranges.
"""

import streamlit as st
import plotly.graph_objects as go


def gauge_chart(title: str, value: float, min_value: float = 0, max_value: float = 100, 
                unit: str = "", color: str = "#00d4ff") -> None:
    """
    Render a gauge chart using Plotly.
    
    Args:
        title: Chart title
        value: Current value
        min_value: Minimum value
        max_value: Maximum value
        unit: Unit label
        color: Gauge color
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': '#ffffff', 'size': 16}},
        number={'suffix': f" {unit}", 'font': {'color': '#ffffff', 'size': 24}},
        gauge={
            'axis': {'range': [min_value, max_value], 'tickwidth': 1, 'tickcolor': "#8892b0"},
            'bar': {'color': color},
            'bgcolor': "#0d1b2a",
            'borderwidth': 2,
            'bordercolor': "#1e3a5f",
            'steps': [
                {'range': [min_value, min_value + (max_value - min_value) * 0.3], 'color': '#1e3a5f'},
                {'range': [min_value + (max_value - min_value) * 0.3, min_value + (max_value - min_value) * 0.7], 'color': '#0d1b2a'},
                {'range': [min_value + (max_value - min_value) * 0.7, max_value], 'color': '#1e3a5f'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': max_value * 0.9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0d1b2a',
        plot_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250
    )
    
    st.plotly_chart(fig, use_container_width=True)


def health_gauge(title: str, value: float) -> None:
    """
    Render a health gauge with color-coded ranges.
    
    Args:
        title: Chart title
        value: Health score (0-100)
    """
    # Determine color based on value
    if value >= 80:
        color = "#00ff88"
    elif value >= 60:
        color = "#ff9800"
    else:
        color = "#ff4444"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': '#ffffff', 'size': 16}},
        number={'suffix': "%", 'font': {'color': color, 'size': 28}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8892b0"},
            'bar': {'color': color},
            'bgcolor': "#0d1b2a",
            'borderwidth': 2,
            'bordercolor': "#1e3a5f",
            'steps': [
                {'range': [0, 50], 'color': '#ff4444'},
                {'range': [50, 80], 'color': '#ff9800'},
                {'range': [80, 100], 'color': '#00ff88'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0d1b2a',
        plot_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250
    )
    
    st.plotly_chart(fig, use_container_width=True)


def progress_gauge(title: str, value: float, max_value: float = 100) -> None:
    """
    Render a progress gauge for showing completion or capacity.
    
    Args:
        title: Chart title
        value: Current value
        max_value: Maximum value
    """
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': '#ffffff', 'size': 16}},
        number={'suffix': "%", 'font': {'color': '#00d4ff', 'size': 28}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8892b0"},
            'bar': {'color': "#00d4ff"},
            'bgcolor': "#0d1b2a",
            'borderwidth': 2,
            'bordercolor': "#1e3a5f",
            'steps': [
                {'range': [0, 25], 'color': '#1e3a5f'},
                {'range': [25, 50], 'color': '#0d1b2a'},
                {'range': [50, 75], 'color': '#1e3a5f'},
                {'range': [75, 100], 'color': '#0d1b2a'}
            ]
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0d1b2a',
        plot_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250
    )
    
    st.plotly_chart(fig, use_container_width=True)
