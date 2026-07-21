"""
Gauges Component

This module provides reusable gauge chart components for displaying metrics.
"""

import streamlit as st
import plotly.graph_objects as go


def gauge_chart(title: str, value: float, min_val: float = 0, max_val: float = 100, 
                color: str = "#00D4FF", unit: str = "") -> None:
    """
    Render a gauge chart.
    
    Args:
        title: Chart title
        value: Current value
        min_val: Minimum value (default: 0)
        max_val: Maximum value (default: 100)
        color: Gauge color (default: cyan)
        unit: Unit string to display (default: empty)
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': '#FFFFFF', 'size': 16}},
        number={'font': {'color': color, 'size': 24}, 'suffix': f" {unit}"},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickcolor': '#B0B0B0', 'tickfont': {'color': '#B0B0B0'}},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, min_val + (max_val - min_val) * 0.3], 'color': '#1E3A5F'},
                {'range': [min_val + (max_val - min_val) * 0.3, min_val + (max_val - min_val) * 0.7], 'color': '#0D1B2A'},
                {'range': [min_val + (max_val - min_val) * 0.7, max_val], 'color': '#1E3A5F'}
            ],
            'threshold': {
                'line': {'color': '#FF0000', 'width': 4},
                'thickness': 0.75,
                'value': max_val * 0.9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0D1B2A',
        margin=dict(l=0, r=0, t=40, b=0),
        height=250
    )
    
    st.plotly_chart(fig, use_container_width=True)


def health_gauge(title: str, health_score: float) -> None:
    """
    Render a health score gauge with color coding.
    
    Args:
        title: Chart title
        health_score: Health score (0-100)
    """
    if health_score >= 80:
        color = "#00FF00"
        status = "Excellent"
    elif health_score >= 60:
        color = "#00D4FF"
        status = "Good"
    elif health_score >= 40:
        color = "#FFA500"
        status = "Fair"
    else:
        color = "#FF0000"
        status = "Poor"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"{title}<br><span style='font-size: 12px; color: {color}'>{status}</span>", 
               'font': {'color': '#FFFFFF', 'size': 16}},
        number={'font': {'color': color, 'size': 28}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#B0B0B0', 'tickfont': {'color': '#B0B0B0'}},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 40], 'color': '#1E3A5F'},
                {'range': [40, 60], 'color': '#0D1B2A'},
                {'range': [60, 80], 'color': '#1E3A5F'},
                {'range': [80, 100], 'color': '#0D1B2A'}
            ],
            'threshold': {
                'line': {'color': color, 'width': 4},
                'thickness': 0.75,
                'value': health_score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0D1B2A',
        margin=dict(l=0, r=0, t=60, b=0),
        height=280
    )
    
    st.plotly_chart(fig, use_container_width=True)


def battery_gauge(title: str, battery_level: float) -> None:
    """
    Render a battery level gauge.
    
    Args:
        title: Chart title
        battery_level: Battery level (0-100)
    """
    if battery_level >= 75:
        color = "#00FF00"
    elif battery_level >= 50:
        color = "#00D4FF"
    elif battery_level >= 25:
        color = "#FFA500"
    else:
        color = "#FF0000"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=battery_level,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': '#FFFFFF', 'size': 16}},
        number={'font': {'color': color, 'size': 24}, 'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#B0B0B0', 'tickfont': {'color': '#B0B0B0'}},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 25], 'color': '#1E3A5F'},
                {'range': [25, 50], 'color': '#0D1B2A'},
                {'range': [50, 75], 'color': '#1E3A5F'},
                {'range': [75, 100], 'color': '#0D1B2A'}
            ],
            'threshold': {
                'line': {'color': '#FF0000', 'width': 4},
                'thickness': 0.75,
                'value': 20
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0D1B2A',
        margin=dict(l=0, r=0, t=40, b=0),
        height=250
    )
    
    st.plotly_chart(fig, use_container_width=True)


def temperature_gauge(title: str, temperature: float, min_temp: float = 0, max_temp: float = 100) -> None:
    """
    Render a temperature gauge with color coding.
    
    Args:
        title: Chart title
        temperature: Temperature value
        min_temp: Minimum temperature (default: 0)
        max_temp: Maximum temperature (default: 100)
    """
    temp_range = max_temp - min_temp
    temp_percent = (temperature - min_temp) / temp_range if temp_range > 0 else 0
    
    if temp_percent >= 0.8:
        color = "#FF0000"
    elif temp_percent >= 0.6:
        color = "#FFA500"
    elif temp_percent >= 0.4:
        color = "#00D4FF"
    else:
        color = "#00FF00"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temperature,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'color': '#FFFFFF', 'size': 16}},
        number={'font': {'color': color, 'size': 24}, 'suffix': "°C"},
        gauge={
            'axis': {'range': [min_temp, max_temp], 'tickcolor': '#B0B0B0', 'tickfont': {'color': '#B0B0B0'}},
            'bar': {'color': color},
            'steps': [
                {'range': [min_temp, min_temp + temp_range * 0.3], 'color': '#1E3A5F'},
                {'range': [min_temp + temp_range * 0.3, min_temp + temp_range * 0.6], 'color': '#0D1B2A'},
                {'range': [min_temp + temp_range * 0.6, min_temp + temp_range * 0.8], 'color': '#1E3A5F'},
                {'range': [min_temp + temp_range * 0.8, max_temp], 'color': '#0D1B2A'}
            ],
            'threshold': {
                'line': {'color': '#FF0000', 'width': 4},
                'thickness': 0.75,
                'value': min_temp + temp_range * 0.9
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='#0D1B2A',
        margin=dict(l=0, r=0, t=40, b=0),
        height=250
    )
    
    st.plotly_chart(fig, use_container_width=True)
