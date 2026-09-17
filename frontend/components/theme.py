"""
AVIONAV Global Theme

Professional industrial aviation design system for Streamlit.
Provides a single source of truth for colors, status badges,
cards, and global CSS.
"""

import streamlit as st


# ---------------------------------------------------------------------------
# AVIONAV COLOR SYSTEM
# ---------------------------------------------------------------------------
COLORS = {
    "background": "#0A1621",
    "surface": "#0E1C2A",
    "card": "#122231",
    "border": "#1E3A4D",
    "primary": "#00C2FF",
    "primary_dark": "#00A0D4",
    "accent": "#00FFCC",
    "white": "#FFFFFF",
    "text": "#B8C7D9",
    "text_muted": "#7C8FA3",
    "success": "#00C853",
    "warning": "#FF9100",
    "error": "#FF4444",
    "info": "#00C2FF",
}


# ---------------------------------------------------------------------------
# STATUS SYSTEM
# ---------------------------------------------------------------------------
STATUS_PALETTE = {
    "HEALTHY": ("HEALTHY", COLORS["success"], "#00C853"),
    "ANOMALY": ("ANOMALY", COLORS["error"], "#FF4444"),
    "WARNING": ("WARNING", COLORS["warning"], "#FF9100"),
    "ACTIVE": ("ACTIVE", COLORS["primary"], "#00C2FF"),
    "OFFLINE": ("OFFLINE", COLORS["text_muted"], "#7C8FA3"),
    "NORMAL": ("NORMAL", COLORS["success"], "#00C853"),
}


def status_badge(status: str) -> str:
    """
    Return a professional HTML status badge.
    """
    label, color, _ = STATUS_PALETTE.get(status, (status, COLORS["info"], COLORS["info"]))
    return f'<span style="display:inline-block;padding:4px 10px;border-radius:4px;font-size:11px;font-weight:600;letter-spacing:0.5px;color:{color};border:1px solid {color};background:{hex_to_rgba(color, 0.08)};">{label}</span>'


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    """Convert a hex color to an rgba string."""
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"


def apply_theme() -> None:
    """
    Inject the global AVIONAV CSS into the Streamlit app.
    Call this from app.py after st.set_page_config.
    """
    st.markdown(
        f"""
        <style>
        /* Global reset */
        html, body, [class*="css"] {{
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .stApp {{
            background: {COLORS["background"]};
        }}

        /* Hide Streamlit top toolbar, deploy button, and header */
        [data-testid="stToolbar"],
        [data-testid="stDeployButton"],
        .stDeployButton,
        .stAppHeader,
        .stToolbar,
        .stApp > header {{
            display: none !important;
        }}

        .stApp {{
            padding-top: 0 !important;
        }}

        [data-testid="stAppViewContainer"] {{
            padding-top: 0 !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: {COLORS["surface"]} !important;
            border-right: 1px solid {COLORS["border"]};
        }}

        [data-testid="stSidebar"] .css-1d391kg {{
            background: {COLORS["surface"]};
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS["white"]} !important;
            font-weight: 600;
        }}

        h2 {{
            font-size: 1.4rem;
            margin-bottom: 0.8rem;
            letter-spacing: 0.2px;
        }}

        h3 {{
            font-size: 1.1rem;
            margin-bottom: 0.6rem;
        }}

        /* Paragraph/caption */
        .stCaption {{
            color: {COLORS["text_muted"]} !important;
        }}

        /* Buttons */
        .stButton > button {{
            border-radius: 6px;
            font-weight: 500;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
        }}

        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 194, 255, 0.15);
        }}

        /* Inputs */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {{
            background: {COLORS["surface"]} !important;
            color: {COLORS["white"]} !important;
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
        }}

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {{
            border-color: {COLORS["primary"]};
            box-shadow: 0 0 0 2px rgba(0, 194, 255, 0.15);
        }}

        /* Selectbox/slider */
        .stSelectbox > div > div > div {{
            background: {COLORS["surface"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 6px;
            color: {COLORS["white"]};
        }}

        .stSlider > div > div > div {{
            color: {COLORS["primary"]};
        }}

        /* Tabs */
        .stTabs [role="tablist"] {{
            background: {COLORS["surface"]};
            border-bottom: 1px solid {COLORS["border"]};
            border-radius: 6px 6px 0 0;
            padding: 4px 8px 0 8px;
        }}

        .stTabs [role="tab"] {{
            color: {COLORS["text"]};
            font-weight: 500;
            font-size: 0.9rem;
            padding: 10px 16px;
        }}

        .stTabs [role="tab"][aria-selected="true"] {{
            color: {COLORS["primary"]};
            border-bottom: 2px solid {COLORS["primary"]};
        }}

        /* Data frames / tables */
        .stDataFrame {{
            background: {COLORS["card"]};
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
        }}

        /* Streamlit info/success/warning/error boxes */
        .stAlert {{
            background: {COLORS["card"]};
            border-radius: 8px;
            border: 1px solid {COLORS["border"]};
        }}

        /* Radio / checkbox */
        .stRadio > div {{
            color: {COLORS["white"]};
        }}

        /* Expander */
        .stExpander {{
            border: 1px solid {COLORS["border"]};
            border-radius: 8px;
            background: {COLORS["card"]};
        }}

        /* Horizontal rule */
        hr {{
            border-color: {COLORS["border"]};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def header_style() -> str:
    """Return CSS for the top header."""
    return f"""
    <style>
    .avionav-header {{
        background: {COLORS["card"]};
        border: 1px solid {COLORS["border"]};
        border-radius: 8px;
        padding: 16px 22px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .avionav-header-title {{
        color: {COLORS["white"]};
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: 0.4px;
        text-transform: uppercase;
        margin: 0;
    }}
    .avionav-header-subtitle {{
        color: {COLORS["text_muted"]};
        font-size: 0.85rem;
        margin: 2px 0 0 0;
    }}
    .avionav-header-meta {{
        text-align: right;
        color: {COLORS["text"]};
        font-size: 0.82rem;
    }}
    .avionav-status-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 6px;
    }}
    </style>
    """
