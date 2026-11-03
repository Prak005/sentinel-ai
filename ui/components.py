"""Reusable Streamlit presentation components."""
import streamlit as st

def metric_card(label, value, note, accent, icon):
    st.markdown(f"""
    <div class="metric-card" style="--accent:{accent}">
        <div class="metric-top">
            <div class="metric-label">{label}</div>
            <div class="metric-icon">{icon}</div>
        </div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def page_header(title, description):
    left, right = st.columns([5, 1])
    with left:
        st.markdown(f"""
        <div class="eyebrow">SECURITY OPERATIONS CENTER</div>
        <div class="main-title">{title}</div>
        <div class="subtitle">{description}</div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("""
        <div class="preview-pill">● UI PREVIEW</div>
        """, unsafe_allow_html=True)

def render_metric_row(metrics):
    cols = st.columns(len(metrics))
    for col, (metric_name, metric_value) in zip(cols, metrics):
        with col:
            st.metric(metric_name, metric_value)
