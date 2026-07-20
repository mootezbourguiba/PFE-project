"""
Cards Component Module

This module provides reusable metric cards for displaying statistics and key metrics.
"""

import streamlit as st


def metric_card(title: str, value: str, icon: str, color: str = "#00d4ff") -> None:
    """
    Render a metric card with title, value, and icon.
    
    Args:
        title: Card title
        value: Card value
        icon: Emoji icon
        color: Accent color (default: cyan)
    """
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
               padding: 20px; border-radius: 15px; margin: 10px 0;
               border: 1px solid {color}; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <div style='color: #8892b0; font-size: 14px; margin-bottom: 5px;'>{title}</div>
                <div style='color: #ffffff; font-size: 32px; font-weight: bold;'>{value}</div>
            </div>
            <div style='font-size: 48px; opacity: 0.8;'>{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def status_card(title: str, status: str, icon: str, is_good: bool = True) -> None:
    """
    Render a status card with good/bad indicator.
    
    Args:
        title: Card title
        status: Status text
        icon: Emoji icon
        is_good: Whether status is good (green) or bad (red)
    """
    color = "#00ff88" if is_good else "#ff4444"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
               padding: 20px; border-radius: 15px; margin: 10px 0;
               border-left: 4px solid {color}; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <div style='color: #8892b0; font-size: 14px; margin-bottom: 5px;'>{title}</div>
                <div style='color: {color}; font-size: 20px; font-weight: bold;'>{status}</div>
            </div>
            <div style='font-size: 36px; opacity: 0.8;'>{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon: str) -> None:
    """
    Render an information card with detailed content.
    
    Args:
        title: Card title
        content: Card content text
        icon: Emoji icon
    """
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
               padding: 20px; border-radius: 15px; margin: 10px 0;
               box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
        <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 10px;'>
            <span style='font-size: 32px;'>{icon}</span>
            <div style='color: #ffffff; font-size: 18px; font-weight: bold;'>{title}</div>
        </div>
        <div style='color: #8892b0; font-size: 14px; line-height: 1.6;'>{content}</div>
    </div>
    """, unsafe_allow_html=True)


def alert_card(title: str, message: str, alert_type: str = "warning") -> None:
    """
    Render an alert card for important notifications.
    
    Args:
        title: Alert title
        message: Alert message
        alert_type: Type of alert (warning, error, info, success)
    """
    colors = {
        "warning": "#ff9800",
        "error": "#ff4444",
        "info": "#2196f3",
        "success": "#00ff88"
    }
    
    icons = {
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️",
        "success": "✅"
    }
    
    color = colors.get(alert_type, "#ff9800")
    icon = icons.get(alert_type, "⚠️")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1e3a5f 0%, #0d1b2a 100%);
               padding: 20px; border-radius: 15px; margin: 10px 0;
               border: 2px solid {color}; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
        <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 10px;'>
            <span style='font-size: 32px;'>{icon}</span>
            <div style='color: {color}; font-size: 18px; font-weight: bold;'>{title}</div>
        </div>
        <div style='color: #ffffff; font-size: 14px; line-height: 1.6;'>{message}</div>
    </div>
    """, unsafe_allow_html=True)
