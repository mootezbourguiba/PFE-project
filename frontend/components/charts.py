"""
Charts Component

This module provides reusable Plotly chart components for data visualization.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any
import pandas as pd


def line_chart(title: str, data: pd.DataFrame, x_col: str, y_col: str, color: str = "#00D4FF") -> None:
    """
    Render a line chart.
    
    Args:
        title: Chart title
        data: DataFrame with chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        color: Line color (default: cyan)
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='lines',
        name=y_col,
        line=dict(color=color, width=2),
        fill='tozeroy',
        fillcolor=f'rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1)'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFFFFF', size=16)),
        xaxis=dict(title=x_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        yaxis=dict(title=y_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        font=dict(color='#B0B0B0'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def bar_chart(title: str, data: pd.DataFrame, x_col: str, y_col: str, color: str = "#00D4FF") -> None:
    """
    Render a bar chart.
    
    Args:
        title: Chart title
        data: DataFrame with chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        color: Bar color (default: cyan)
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data[x_col],
        y=data[y_col],
        marker_color=color,
        marker_line_color=color,
        marker_line_width=2
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFFFFF', size=16)),
        xaxis=dict(title=x_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        yaxis=dict(title=y_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        font=dict(color='#B0B0B0'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def pie_chart(title: str, data: pd.DataFrame, names_col: str, values_col: str) -> None:
    """
    Render a pie chart.
    
    Args:
        title: Chart title
        data: DataFrame with chart data
        names_col: Column name for pie slices
        values_col: Column name for values
    """
    colors = ['#00D4FF', '#00FF00', '#FFA500', '#FF0000', '#FF00FF', '#FFFF00']
    
    fig = go.Figure(data=[go.Pie(
        labels=data[names_col],
        values=data[values_col],
        hole=0.3,
        marker=dict(colors=colors[:len(data)]),
        textinfo='label+percent',
        textfont=dict(color='#FFFFFF')
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFFFFF', size=16)),
        paper_bgcolor='#0D1B2A',
        font=dict(color='#B0B0B0'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def scatter_chart(title: str, data: pd.DataFrame, x_col: str, y_col: str, color: str = "#00D4FF") -> None:
    """
    Render a scatter chart.
    
    Args:
        title: Chart title
        data: DataFrame with chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        color: Point color (default: cyan)
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data[x_col],
        y=data[y_col],
        mode='markers',
        marker=dict(color=color, size=8, line=dict(color='#FFFFFF', width=1))
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFFFFF', size=16)),
        xaxis=dict(title=x_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        yaxis=dict(title=y_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        font=dict(color='#B0B0B0'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)


def multi_line_chart(title: str, data: pd.DataFrame, x_col: str, y_cols: List[str], colors: List[str] = None) -> None:
    """
    Render a multi-line chart.
    
    Args:
        title: Chart title
        data: DataFrame with chart data
        x_col: Column name for x-axis
        y_cols: List of column names for y-axis
        colors: List of colors for each line (default: cyan theme)
    """
    if colors is None:
        colors = ['#00D4FF', '#00FF00', '#FFA500', '#FF0000', '#FF00FF']
    
    fig = go.Figure()
    
    for i, y_col in enumerate(y_cols):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            mode='lines',
            name=y_col,
            line=dict(color=color, width=2)
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFFFFF', size=16)),
        xaxis=dict(title=x_col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        yaxis=dict(title='Value', gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        font=dict(color='#B0B0B0'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def histogram(title: str, data: pd.DataFrame, col: str, color: str = "#00D4FF") -> None:
    """
    Render a histogram.
    
    Args:
        title: Chart title
        data: DataFrame with chart data
        col: Column name for histogram
        color: Bar color (default: cyan)
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=data[col],
        marker_color=color,
        marker_line_color=color,
        marker_line_width=2,
        nbinsx=20
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color='#FFFFFF', size=16)),
        xaxis=dict(title=col, gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        yaxis=dict(title='Count', gridcolor='#1E3A5F', tickcolor='#B0B0B0'),
        plot_bgcolor='#0D1B2A',
        paper_bgcolor='#0D1B2A',
        font=dict(color='#B0B0B0'),
        margin=dict(l=0, r=0, t=40, b=0),
        height=300
    )
    
    st.plotly_chart(fig, use_container_width=True)
