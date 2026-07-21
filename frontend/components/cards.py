"""
Cards Component

This module provides reusable card components for displaying metrics and information.
"""

import streamlit as st


def metric_card(title: str, value: str, icon: str, color: str = "#00D4FF") -> None:
    """
    Render a metric card with title, value, and icon.
    
    Args:
        title: Card title
        value: Card value
        icon: Icon emoji
        color: Accent color (default: cyan)
    """
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px; border-radius: 15px; margin: 10px 0; 
               border: 1px solid {color}; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <p style='color: #808080; font-size: 12px; margin: 0;'>{title}</p>
                <p style='color: #FFFFFF; font-size: 28px; font-weight: bold; margin: 5px 0;'>{value}</p>
            </div>
            <div style='font-size: 40px; color: {color};'>{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def info_card(title: str, content: str, icon: str = "ℹ️") -> None:
    """
    Render an information card with title and content.
    
    Args:
        title: Card title
        content: Card content
        icon: Icon emoji (default: info)
    """
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px; border-radius: 15px; margin: 10px 0;'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
            <span style='font-size: 24px;'>{icon}</span>
            <h3 style='color: #00D4FF; font-size: 16px; margin: 0;'>{title}</h3>
        </div>
        <p style='color: #B0B0B0; font-size: 14px; margin: 0;'>{content}</p>
    </div>
    """, unsafe_allow_html=True)


def status_card(title: str, status: str, status_color: str = "#00FF00") -> None:
    """
    Render a status card with title and status indicator.
    
    Args:
        title: Card title
        status: Status text
        status_color: Status color (default: green)
    """
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px; border-radius: 15px; margin: 10px 0;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <p style='color: #FFFFFF; font-size: 16px; font-weight: bold; margin: 0;'>{title}</p>
            <div style='display: flex; align-items: center; gap: 8px;'>
                <div style='width: 12px; height: 12px; border-radius: 50%; 
                           background: {status_color}; box-shadow: 0 0 10px {status_color};'></div>
                <p style='color: {status_color}; font-size: 14px; font-weight: bold; margin: 0;'>{status}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def alert_card(title: str, message: str, alert_type: str = "warning") -> None:
    """
    Render an alert card with title and message.
    
    Args:
        title: Alert title
        message: Alert message
        alert_type: Alert type (warning, error, info, success)
    """
    colors = {
        "warning": "#FFA500",
        "error": "#FF0000",
        "info": "#00D4FF",
        "success": "#00FF00"
    }
    
    icons = {
        "warning": "⚠️",
        "error": "❌",
        "info": "ℹ️",
        "success": "✅"
    }
    
    color = colors.get(alert_type, "#FFA500")
    icon = icons.get(alert_type, "⚠️")
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px; border-radius: 15px; margin: 10px 0; 
               border-left: 4px solid {color};'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
            <span style='font-size: 24px;'>{icon}</span>
            <h3 style='color: {color}; font-size: 16px; margin: 0;'>{title}</h3>
        </div>
        <p style='color: #B0B0B0; font-size: 14px; margin: 0;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)


def prediction_card(title: str, prediction: str, confidence: float, recommendation: str) -> None:
    """
    Render a prediction card with AI model results.
    
    Args:
        title: Card title
        prediction: Prediction result
        confidence: Confidence score (0-100)
        recommendation: AI recommendation
    """
    confidence_color = "#00FF00" if confidence > 70 else "#FFA500" if confidence > 50 else "#FF0000"
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #1E3A5F 0%, #0D1B2A 100%); 
               padding: 20px; border-radius: 15px; margin: 10px 0; 
               border: 2px solid #00D4FF;'>
        <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 15px;'>
            <span style='font-size: 24px;'>🤖</span>
            <h3 style='color: #00D4FF; font-size: 16px; margin: 0;'>{title}</h3>
        </div>
        <div style='margin-bottom: 15px;'>
            <p style='color: #808080; font-size: 12px; margin: 0;'>Prediction</p>
            <p style='color: #FFFFFF; font-size: 18px; font-weight: bold; margin: 5px 0;'>{prediction}</p>
        </div>
        <div style='margin-bottom: 15px;'>
            <p style='color: #808080; font-size: 12px; margin: 0;'>Confidence</p>
            <div style='background: #0D1B2A; height: 8px; border-radius: 4px; margin: 5px 0;'>
                <div style='background: {confidence_color}; height: 100%; border-radius: 4px; 
                           width: {confidence}%;'></div>
            </div>
            <p style='color: {confidence_color}; font-size: 14px; font-weight: bold; margin: 5px 0;'>{confidence:.1f}%</p>
        </div>
        <div>
            <p style='color: #808080; font-size: 12px; margin: 0;'>Recommendation</p>
            <p style='color: #00FF00; font-size: 14px; margin: 5px 0;'>{recommendation}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
