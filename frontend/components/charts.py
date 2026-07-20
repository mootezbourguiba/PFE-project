"""
Charts Component Module

This module provides reusable Plotly charts for data visualization.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import pandas as pd


def line_chart(title: str, x_data: List, y_data: List, x_label: str = "", y_label: str = "", color: str = "#00d4ff") -> None:
    """
    Render a line chart using Plotly.
    
    Args:
        title: Chart title
        x_data: X-axis data
        y_data: Y-axis data
        x_label: X-axis label
        y_label: Y-axis label
        color: Line color
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        name=title,
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#ffffff', size=18)),
        xaxis=dict(title=x_label, color='#8892b0', gridcolor='#1e3a5f'),
        yaxis=dict(title=y_label, color='#8892b0', gridcolor='#1e3a5f'),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=50, r=50, t=50, b=50),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def bar_chart(title: str, labels: List, values: List, color: str = "#00d4ff") -> None:
    """
    Render a bar chart using Plotly.
    
    Args:
        title: Chart title
        labels: Bar labels
        values: Bar values
        color: Bar color
    """
    fig = go.Figure(data=[go.Bar(
        x=labels,
        y=values,
        marker=dict(color=color),
        text=values,
        textposition='auto'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#ffffff', size=18)),
        xaxis=dict(color='#8892b0', gridcolor='#1e3a5f'),
        yaxis=dict(color='#8892b0', gridcolor='#1e3a5f'),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=50, r=50, t=50, b=50),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def pie_chart(title: str, labels: List, values: List, colors: List = None) -> None:
    """
    Render a pie chart using Plotly.
    
    Args:
        title: Chart title
        labels: Pie slice labels
        values: Pie slice values
        colors: Custom colors (optional)
    """
    if colors is None:
        colors = ['#00d4ff', '#00ff88', '#ff9800', '#ff4444', '#9c27b0']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        hole=0.3
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#ffffff', size=18)),
        paper_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=50, r=50, t=50, b=50),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def scatter_chart(title: str, x_data: List, y_data: List, x_label: str = "", y_label: str = "", color: str = "#00d4ff") -> None:
    """
    Render a scatter chart using Plotly.
    
    Args:
        title: Chart title
        x_data: X-axis data
        y_data: Y-axis data
        x_label: X-axis label
        y_label: Y-axis label
        color: Point color
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='markers',
        name=title,
        marker=dict(color=color, size=8)
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#ffffff', size=18)),
        xaxis=dict(title=x_label, color='#8892b0', gridcolor='#1e3a5f'),
        yaxis=dict(title=y_label, color='#8892b0', gridcolor='#1e3a5f'),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=50, r=50, t=50, b=50),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def multi_line_chart(title: str, data: Dict[str, List], x_label: str = "", y_label: str = "") -> None:
    """
    Render a multi-line chart using Plotly.
    
    Args:
        title: Chart title
        data: Dictionary with series names as keys and values as lists
        x_label: X-axis label
        y_label: Y-axis label
    """
    colors = ['#00d4ff', '#00ff88', '#ff9800', '#ff4444', '#9c27b0']
    
    fig = go.Figure()
    
    for i, (name, values) in enumerate(data.items()):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=list(range(len(values))),
            y=values,
            mode='lines',
            name=name,
            line=dict(color=color, width=2)
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#ffffff', size=18)),
        xaxis=dict(title=x_label, color='#8892b0', gridcolor='#1e3a5f'),
        yaxis=dict(title=y_label, color='#8892b0', gridcolor='#1e3a5f'),
        plot_bgcolor='#0d1b2a',
        paper_bgcolor='#0d1b2a',
        font=dict(color='#8892b0'),
        margin=dict(l=50, r=50, t=50, b=50),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
