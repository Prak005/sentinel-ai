
"""Anomaly Monitor page for Sentinel AI."""

from html import escape

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ui.components import page_header


ANOMALY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ===== ANOMALY MONITOR PAGE ===== */

.am-intro {
    background: linear-gradient(115deg, rgba(20, 37, 59, 0.95), rgba(13, 25, 43, 0.95));
    border: 1px solid rgba(87, 230, 224, 0.18);
    border-radius: 16px;
    padding: 25px 28px;
    margin: 12px 0 28px 0;
}

.am-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 9px;
    font-family: 'Rajdhani', sans-serif;
}

.am-intro-title {
    color: #F1F6FF;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 8px;
    line-height: 1.3;
    font-family: 'Orbitron', sans-serif;
}

.am-intro-copy {
    color: #A8B8CB;
    font-size: 17px;
    line-height: 1.7;
    margin: 0;
    font-family: 'Rajdhani', sans-serif;
}

/* Section headings */

.am-section {
    margin: 24px 0 16px 0;
}

.am-section-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-bottom: 5px;
    font-family: 'Rajdhani', sans-serif;
}

.am-section-title {
    color: #F1F6FF;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.4;
    font-family: 'Orbitron', sans-serif;
}

.am-section-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.6;
    margin-top: 4px;
    font-family: 'Rajdhani', sans-serif;
}

/* Metric cards */

.am-metric-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-left: 4px solid var(--am-accent);
    border-radius: 13px;
    padding: 21px 20px;
    min-height: 135px;
}

.am-metric-label {
    color: #A8B8CB;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
    font-family: 'Rajdhani', sans-serif;
}

.am-metric-value {
    color: #F1F6FF;
    font-size: 31px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.am-metric-note {
    color: #879AB1;
    font-size: 14px;
    line-height: 1.5;
    font-family: 'Rajdhani', sans-serif;
}

/* Panels */

.am-panel-title {
    color: #F1F6FF;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 5px;
    font-family: 'Orbitron', sans-serif;
}

.am-panel-subtitle {
    color: #93A6BC;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 15px;
    font-family: 'Rajdhani', sans-serif;
}

.am-chip {
    display: inline-block;
    background: rgba(87, 230, 224, 0.09);
    color: #57E6E0;
    border: 1px solid rgba(87, 230, 224, 0.24);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    font-family: 'Rajdhani', sans-serif;
}

/* Score information */

.am-score-box {
    background: rgba(87, 230, 224, 0.045);
    border: 1px solid rgba(87, 230, 224, 0.16);
    border-radius: 11px;
    padding: 15px 16px;
    margin: 12px 0;
    color: #C4D2E2;
    font-size: 16px;
    line-height: 1.75;
    font-family: 'Rajdhani', sans-serif;
}

.am-normal {
    color: #45D6C2;
    font-weight: 700;
}

.am-anomaly {
    color: #FF9292;
    font-weight: 700;
}

/* Empty state and note */

.am-empty {
    background: rgba(87, 230, 224, 0.05);
    border: 1px solid rgba(87, 230, 224, 0.20);
    border-radius: 14px;
    padding: 24px;
    margin: 20px 0;
}

.am-empty-title {
    color: #EAF3FF;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.am-empty-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.7;
    font-family: 'Rajdhani', sans-serif;
}

.am-note {
    background: rgba(255, 184, 107, 0.055);
    border-left: 3px solid #FFB86B;
    border-radius: 7px;
    padding: 14px 17px;
    color: #B9C5D5;
    font-size: 15px;
    line-height: 1.7;
    margin-top: 18px;
    font-family: 'Rajdhani', sans-serif;
}

/* Consistent Streamlit typography */

.main .stMarkdown p,
.main .stMarkdown li,
.main [data-testid="stCaptionContainer"] {
    font-size: 16px !important;
    line-height: 1.65 !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main label {
    font-size: 16px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main .stButton button,
.main .stDownloadButton button {
    font-size: 16px !important;
    min-height: 47px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main [data-testid="stDataFrame"] {
    font-size: 15px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main [data-testid="stMetricLabel"] {
    font-size: 15px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

.main [data-testid="stMetricValue"] {
    font-size: 29px !important;
    font-family: 'Orbitron', sans-serif !important;
}

/* Plotly chart typography */

.main .js-plotly-plot .xtick text,
.main .js-plotly-plot .ytick text,
.main .js-plotly-plot .legend text {
    font-size: 14px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

</style>
"""


def metric_card(label, value, note, accent):
    return f"""
    <div class="am-metric-card" style="--am-accent:{accent}">
        <div class="am-metric-label">{escape(label)}</div>
        <div class="am-metric-value">{escape(str(value))}</div>
        <div class="am-metric-note">{escape(note)}</div>
    </div>
    """


def render_page():

    st.markdown(ANOMALY_CSS, unsafe_allow_html=True)

    page_header(
        "Anomaly Monitor",
        "Identify unusual network behaviour using the Isolation Forest algorithm."
    )

    st.markdown("""
    <div class="am-intro">
        <div class="am-kicker">SECURITY INTELLIGENCE / ANOMALY MONITORING</div>
        <div class="am-intro-title">Behavioural Anomaly Analysis</div>
        <p class="am-intro-copy">
            Monitor unusual network-flow behaviour using Isolation Forest.
            Examine anomaly scores, distinguish suspicious traffic from
            known attacks and investigate the flagged records.
        </p>
    </div>
    """, unsafe_allow_html=True)

    analysis_df = st.session_state.get("sentinel_analysis_df")

    if analysis_df is None:

        st.markdown("""
        <div class="am-empty">
            <div class="am-empty-title">No Analysis Available</div>
            <div class="am-empty-copy">
                No traffic analysis has been performed yet.
                Visit Traffic Analyzer, upload a network-flow CSV
                and run the hybrid analysis to monitor anomalies here.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Anomaly monitoring results will appear here after traffic analysis."
        )

    else:

        # Keep compact boolean masks for summary statistics. Materialize
        # filtered DataFrames only when the user reaches the report section.
        anomaly_mask = analysis_df["IF Prediction"] == "Anomaly"
        suspicious_mask = analysis_df["Final Status"] == "Suspicious Anomaly"
        known_attack_anomalies_mask = (
            anomaly_mask & (analysis_df["Final Status"] == "Known Attack")
        )
        normal_mask = analysis_df["IF Prediction"] == "Normal"

        anomaly_count = int(anomaly_mask.sum())
        suspicious_count = int(suspicious_mask.sum())
        known_attack_anomaly_count = int(known_attack_anomalies_mask.sum())
        normal_count = int(normal_mask.sum())

        # Anomaly summary

        st.markdown("""
        <div class="am-section">
            <div class="am-section-kicker">DETECTION OVERVIEW</div>
            <div class="am-section-title">Anomaly Detection Summary</div>
            <div class="am-section-copy">
                Overview of unusual traffic identified by Isolation Forest.
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4, gap="medium")

        with m1:
            st.markdown(
                metric_card(
                    "IF Flagged Flows",
                    f"{anomaly_count:,}",
                    "Total records flagged as anomalous",
                    "#FF7777"
                ),
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                metric_card(
                    "Suspicious Anomalies",
                    f"{suspicious_count:,}",
                    "Hybrid detection classified as suspicious",
                    "#FFB86B"
                ),
                unsafe_allow_html=True
            )

        with m3:
            st.markdown(
                metric_card(
                    "Known Attacks Also Flagged",
                    f"{known_attack_anomaly_count:,}",
                    "Known attacks also flagged by IF",
                    "#FF7777"
                ),
                unsafe_allow_html=True
            )

        with m4:
            st.markdown(
                metric_card(
                    "IF Normal Flows",
                    f"{normal_count:,}",
                    "Records classified as normal by IF",
                    "#45D6C2"
                ),
                unsafe_allow_html=True
            )

        st.write("")

        # Anomaly score distribution

        chart_col, info_col = st.columns(
            [1.4, 1],
            gap="medium"
        )

        with chart_col:

            with st.container(border=True):

                st.markdown("""
                <div class="am-panel-title">Anomaly Score Distribution</div>
                <div class="am-panel-subtitle">
                    Comparison of normal and Isolation Forest flagged traffic.
                </div>
                """, unsafe_allow_html=True)

                # The inference pipeline already stores numeric anomaly
                # scores. Avoid copying the complete analyzed dataset just
                # to build the two histogram series.
                score_series = analysis_df["Anomaly Score"]

                normal_scores = score_series.loc[
                    analysis_df["IF Prediction"] == "Normal"
                ].dropna()

                anomaly_scores = score_series.loc[
                    analysis_df["IF Prediction"] == "Anomaly"
                ].dropna()

                fig = go.Figure()

                if not normal_scores.empty:

                    fig.add_trace(
                        go.Histogram(
                            x=normal_scores,
                            name="Normal",
                            marker_color="#45D6C2",
                            opacity=0.70
                        )
                    )

                if not anomaly_scores.empty:

                    fig.add_trace(
                        go.Histogram(
                            x=anomaly_scores,
                            name="Anomaly",
                            marker_color="#FF7777",
                            opacity=0.70
                        )
                    )

                fig.update_layout(
                    height=340,
                    barmode="overlay",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        family="Rajdhani, sans-serif",
                        color="#A8B8CB",
                        size=14
                    ),
                    margin=dict(l=10, r=15, t=25, b=15),
                    xaxis=dict(
                        title="Anomaly Score",
                        showgrid=False,
                        title_font=dict(size=16),
                        automargin=True
                    ),
                    yaxis=dict(
                        title="Number of Flows",
                        showgrid=True,
                        gridcolor="rgba(148,163,184,0.10)",
                        title_font=dict(size=16),
                        automargin=True
                    ),
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1,
                        font=dict(size=14)
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

        # Understanding anomaly scores

        with info_col:

            with st.container(border=True):

                st.markdown(
                    '<div class="am-score-box">'
                    '<b class="am-normal">● Normal Traffic</b><br>'
                    'Isolation Forest prediction: <b>1</b><br><br>'
                    '<b class="am-anomaly">● Anomalous Traffic</b><br>'
                    'Isolation Forest prediction: <b>-1</b>'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="am-score-box">'
                    '<b>Score Interpretation</b><br>'
                    'Lower anomaly scores indicate more unusual '
                    'observations in the model\'s scoring system.'
                    '</div>',
                    unsafe_allow_html=True
                )

                score_values = score_series.dropna()

                if not score_values.empty:

                    st.metric(
                        "Lowest Anomaly Score",
                        f"{score_values.min():.4f}"
                    )

                    st.metric(
                        "Highest Anomaly Score",
                        f"{score_values.max():.4f}"
                    )

        st.write("")

        # Flagged traffic records

        with st.container(border=True):

            st.markdown("""
            <div class="am-section-kicker">INVESTIGATION CONSOLE</div>
            <div class="am-panel-title">Flagged Traffic Records</div>
            <div class="am-panel-subtitle">
                Isolation Forest anomalies, sorted from lowest anomaly score upward.
            </div>
            """, unsafe_allow_html=True)

            if anomaly_count == 0:

                st.success(
                    "No anomalous traffic was flagged in the latest analysis."
                )

            else:

                # Create the report subset only at the point it is needed.
                anomaly_df = analysis_df.loc[anomaly_mask].sort_values(
                    "Anomaly Score",
                    ascending=True
                )

                st.markdown(
                    f"""
                    <div class="am-panel-subtitle">
                        <b>{len(anomaly_df):,}</b> anomalous records identified
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.dataframe(
                    anomaly_df.head(200),
                    use_container_width=True,
                    hide_index=True
                )

                if len(anomaly_df) > 200:

                    st.caption(
                        "Showing first 200 records. "
                        "Download the report for all flagged records."
                    )

                st.download_button(
                    "⬇️ Download Anomaly Report",
                    data=lambda: anomaly_df.to_csv(index=False).encode("utf-8"),
                    file_name="sentinel_ai_anomaly_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        st.markdown("""
        <div class="am-note">
            <b>IMPORTANT:</b> Isolation Forest may flag both known attacks
            and unusual benign traffic. The Hybrid Detection result
            distinguishes Known Attack from Suspicious Anomaly.
        </div>
        """, unsafe_allow_html=True)
