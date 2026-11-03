"""Sentinel AI Streamlit application entry point."""
import streamlit as st
from ui.styles import CUSTOM_CSS
from views import overview, traffic_analyzer, threat_detection, anomaly_monitor, model_performance, dataset_explorer

st.set_page_config(
    page_title="Sentinel AI- The ultimate defender",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(f"<style>{CUSTOM_CSS}</style>", unsafe_allow_html=True)

with st.sidebar:
    # Brand header: visual-only component. Keep the title/subtitle here editable.
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M24 4.5L39 10V21.2C39 31.2 32.8 39.1 24 43.5C15.2 39.1 9 31.2 9 21.2V10L24 4.5Z"
                      stroke="#62E8D9" stroke-width="2.2" stroke-linejoin="round"/>
                <path d="M17 23.5L21.5 28L31.5 17.5"
                      stroke="#E9FFFC" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M24 9.5L34.5 13.4V21C34.5 28.1 30.4 34.1 24 37.7"
                      stroke="#62E8D9" stroke-opacity="0.35" stroke-width="1.2" stroke-linecap="round"/>
            </svg>
        </div>
        <div class="brand-copy">
            <div class="brand-name"><span>SENTINEL</span><span class="brand-ai">AI</span></div>
            <div class="brand-subtitle">THE ULTIMATE DEFENDER</div>
        </div>
    </div>
    <div class="brand-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="side-label">WORKSPACE</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Traffic Analyzer",
            "Threat Detection",
            "Anomaly Monitor",
            "Model Performance",
            "Dataset Explorer"
        ],
        label_visibility="collapsed"
    )

    # CUSTOM FOOTER: Replace the placeholder title and text below with your own content.
    st.markdown("""
    <div class="sidebar-footer">
        <div class="footer-title">ALL IN ONE DEFENDER</div>
        <div class="footer-text">By Sentinel AI Team</div>
    </div>
    """, unsafe_allow_html=True)

PAGE_RENDERERS = {
    "Overview": overview.render_page,
    "Traffic Analyzer": traffic_analyzer.render_page,
    "Threat Detection": threat_detection.render_page,
    "Anomaly Monitor": anomaly_monitor.render_page,
    "Model Performance": model_performance.render_page,
    "Dataset Explorer": dataset_explorer.render_page,
}
PAGE_RENDERERS[page]()

# -----------------------------------

st.markdown("""
<div class="app-footer">
    SENTINEL AI · INTELLIGENT NETWORK INTRUSION DETECTION SYSTEM
    <br><br>
    Machine Learning Based Network Security Monitoring
    <br>
    UI Preview Version 1.0
</div>
""", unsafe_allow_html=True)

