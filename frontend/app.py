import streamlit as st
from PIL import Image
from pathlib import Path

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="AVIONAV Platform",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# Assets
# -------------------------------------------------------

ASSETS = Path(__file__).parent / "assets"

logo = Image.open(ASSETS / "images" / "avionav_logo.png")
banner = Image.open(ASSETS / "images" / "banner.jpg")

# -------------------------------------------------------
# Custom CSS
# -------------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
}

h1,h2,h3{
    color:#0B3C5D;
}

.metric-card{
    background:#F7F9FB;
    padding:20px;
    border-radius:12px;
    border-left:6px solid #0B3C5D;
    box-shadow:0px 4px 10px rgba(0,0,0,.08);
    text-align:center;
}

.section-title{
    font-size:28px;
    font-weight:bold;
    color:#0B3C5D;
}

.footer{
    text-align:center;
    color:gray;
    padding-top:40px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

c1, c2 = st.columns([1,5])

with c1:
    st.image(logo, width=150)

with c2:
    st.title("AVIONAV")
    st.subheader("Intelligent UAV Health Monitoring & Predictive Maintenance Platform")

st.divider()

# -------------------------------------------------------
# Banner
# -------------------------------------------------------

st.image(
    banner,
    use_container_width=True
)

# -------------------------------------------------------
# Hero
# -------------------------------------------------------

st.markdown(
"""
# Intelligent Avionics Monitoring

The AVIONAV platform is designed to monitor UAV propulsion health in
real time using Artificial Intelligence.

The system continuously analyses motor current and temperature,
detects abnormal behaviour and assists maintenance engineers
before failures occur.

"""
)

st.divider()

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

st.markdown(
'<p class="section-title">Platform Overview</p>',
unsafe_allow_html=True
)

c1,c2,c3,c4=st.columns(4)

with c1:
    st.markdown(
    """
    <div class="metric-card">
    <h2>👥</h2>
    <h3>Users</h3>
    <h1>3</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

with c2:
    st.markdown(
    """
    <div class="metric-card">
    <h2>✈️</h2>
    <h3>Flights</h3>
    <h1>0</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

with c3:
    st.markdown(
    """
    <div class="metric-card">
    <h2>🚨</h2>
    <h3>Alerts</h3>
    <h1>0</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

with c4:
    st.markdown(
    """
    <div class="metric-card">
    <h2>🤖</h2>
    <h3>AI Models</h3>
    <h1>1</h1>
    </div>
    """,
    unsafe_allow_html=True
    )

st.divider()

# -------------------------------------------------------
# Platform Modules
# -------------------------------------------------------

st.markdown(
'<p class="section-title">Platform Modules</p>',
unsafe_allow_html=True
)

left,right=st.columns(2)

with left:

    st.info("👤 **Administrator**")
    st.write("""
- Manage users
- Configure the platform
- View system statistics
- Manage roles
""")

    st.info("🛠 **Maintenance Engineer**")
    st.write("""
- Monitor telemetry
- Detect anomalies
- Review flight history
- Analyse AI predictions
""")

with right:

    st.info("🎮 **Drone Operator**")
    st.write("""
- Monitor flight status
- View alerts
- Check motor health
- Receive warnings
""")

    st.info("🤖 **Artificial Intelligence**")
    st.write("""
- Isolation Forest
- Bearing wear detection
- Real-time anomaly detection
- Predictive maintenance
""")

st.divider()

# -------------------------------------------------------
# Technologies
# -------------------------------------------------------

st.markdown(
'<p class="section-title">Technology Stack</p>',
unsafe_allow_html=True
)

st.columns(6)

c1,c2,c3,c4,c5,c6=st.columns(6)

c1.success("🐍 Python")

c2.success("⚡ FastAPI")

c3.success("🎈 Streamlit")

c4.success("🗄 SQLite")

c5.success("🤖 Scikit-Learn")

c6.success("📊 Plotly")

st.divider()

st.markdown(
"""
<div class="footer">

© 2026 AVIONAV • Intelligent UAV Health Monitoring Platform

Developed as a Final Year Engineering Project

</div>
""",
unsafe_allow_html=True
)