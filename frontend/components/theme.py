import streamlit as st


def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )


def page_header(title, subtitle):
    st.markdown(
        f"""
<div class='title'>{title}</div>
<div class='subtitle'>{subtitle}</div>
""",
        unsafe_allow_html=True,
    )