
"""Threat Detection page for Sentinel AI."""

from html import escape

import streamlit as st
import plotly.graph_objects as go

from ui.components import page_header


THREAT_CSS = """
<style>
/* ===== THREAT DETECTION PAGE ===== */

.td-intro {
    background: linear-gradient(115deg, rgba(20, 37, 59, 0.95), rgba(13, 25, 43, 0.95));
    border: 1px solid rgba(87, 230, 224, 0.18);
    border-radius: 16px;
    padding: 25px 28px;
    margin: 12px 0 28px 0;
}

.td-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 9px;
}

.td-intro-title {
    color: #F1F6FF;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 8px;
    line-height: 1.3;
}

.td-intro-copy {
    color: #A8B8CB;
    font-size: 17px;
    line-height: 1.7;
    margin: 0;
}

.td-section {
    margin: 24px 0 16px 0;
}

.td-section-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-bottom: 5px;
}

.td-section-title {
    color: #F1F6FF;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.4;
}

.td-section-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.6;
    margin-top: 4px;
}

/* Metric cards */

.td-metric-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-left: 4px solid var(--td-accent);
    border-radius: 13px;
    padding: 21px 20px;
    min-height: 135px;
}

.td-metric-label {
    color: #A8B8CB;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
}

.td-metric-value {
    color: #F1F6FF;
    font-size: 31px;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 8px;
}

.td-metric-note {
    color: #879AB1;
    font-size: 14px;
    line-height: 1.5;
}

/* Panel headings */

.td-panel-title {
    color: #F1F6FF;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 5px;
}

.td-panel-subtitle {
    color: #93A6BC;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 15px;
}

.td-chip {
    display: inline-block;
    background: rgba(255, 119, 119, 0.10);
    color: #FF9292;
    border: 1px solid rgba(255, 119, 119, 0.24);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
}

.td-record-count {
    color: #A8B8CB;
    font-size: 15px;
    margin: 10px 0 14px 0;
    line-height: 1.6;
}

/* Empty state */

.td-empty {
    background: rgba(87, 230, 224, 0.05);
    border: 1px solid rgba(87, 230, 224, 0.20);
    border-radius: 14px;
    padding: 24px;
    margin: 20px 0;
}

.td-empty-title {
    color: #EAF3FF;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 8px;
}

.td-empty-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.7;
}

/* Readability */

.main .stMarkdown p,
.main .stMarkdown li,
.main [data-testid="stCaptionContainer"] {
    font-size: 16px !important;
    line-height: 1.65 !important;
}

.main label {
    font-size: 16px !important;
}

.main div[data-baseweb="select"] * {
    font-size: 16px !important;
}

.main .stButton button,
.main .stDownloadButton button {
    font-size: 16px !important;
    min-height: 47px !important;
}

.main [data-testid="stDataFrame"] {
    font-size: 15px !important;
}

.main [data-testid="stMetricLabel"] {
    font-size: 15px !important;
}

.main [data-testid="stMetricValue"] {
    font-size: 29px !important;
}

.main .js-plotly-plot .xtick text,
.main .js-plotly-plot .ytick text {
    font-size: 14px !important;
}

</style>
"""


def metric_card(label, value, note, accent):
    return f"""
    <div class="td-metric-card" style="--td-accent:{accent}">
        <div class="td-metric-label">{escape(label)}</div>
        <div class="td-metric-value">{escape(str(value))}</div>
        <div class="td-metric-note">{escape(note)}</div>
    </div>
    """


def render_page():

    st.markdown(THREAT_CSS, unsafe_allow_html=True)

    page_header(
        "Threat Detection",
        "Explore known network attacks identified by the Random Forest classifier."
    )

    st.markdown("""
    <div class="td-intro">
        <div class="td-kicker">SECURITY INTELLIGENCE / THREAT MONITORING</div>
        <div class="td-intro-title">Known Attack Intelligence</div>
        <p class="td-intro-copy">
            Identify, classify and investigate malicious network traffic.
            Review attack categories and inspect the individual records
            flagged by the Random Forest classifier.
        </p>
    </div>
    """, unsafe_allow_html=True)

    analysis_df = st.session_state.get("sentinel_analysis_df")

    if analysis_df is None:

        st.markdown("""
        <div class="td-empty">
            <div class="td-empty-title">No Analysis Available</div>
            <div class="td-empty-copy">
                No traffic analysis has been performed yet.
                Visit the Traffic Analyzer, upload a network-flow CSV
                and run the hybrid analysis to view threat intelligence here.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "Your detected threats will appear here after traffic analysis."
        )

    else:

        # Keep a boolean mask instead of copying every known-attack row.
        known_attack_mask = analysis_df["Final Status"] == "Known Attack"
        attack_predictions = analysis_df.loc[known_attack_mask, "RF Prediction"]
        total_attacks = int(known_attack_mask.sum())

        if total_attacks == 0:

            st.success(
                "No known attacks detected in the latest analyzed dataset."
            )

            st.caption(
                "This means Random Forest classified all uploaded records "
                "as BENIGN. Check Anomaly Monitor separately for unusual traffic."
            )

        else:

            # Attack statistics

            attack_counts = attack_predictions.value_counts()

            unique_attacks = len(attack_counts)

            also_flagged = int(
                (
                    known_attack_mask
                    & (analysis_df["IF Prediction"] == "Anomaly")
                ).sum()
            )

            # Threat summary

            st.markdown("""
            <div class="td-section">
                <div class="td-section-kicker">THREAT OVERVIEW</div>
                <div class="td-section-title">Threat Intelligence Summary</div>
                <div class="td-section-copy">
                    A snapshot of known malicious traffic detected in the dataset.
                </div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3, gap="medium")

            with m1:
                st.markdown(
                    metric_card(
                        "Known Attack Flows",
                        f"{total_attacks:,}",
                        "Records classified as malicious",
                        "#FF7777"
                    ),
                    unsafe_allow_html=True
                )

            with m2:
                st.markdown(
                    metric_card(
                        "Attack Categories",
                        f"{unique_attacks:,}",
                        "Distinct attack types identified",
                        "#FFB86B"
                    ),
                    unsafe_allow_html=True
                )

            with m3:
                st.markdown(
                    metric_card(
                        "Also Flagged by IF",
                        f"{also_flagged:,}",
                        "Known attacks also flagged as anomalies",
                        "#57E6E0"
                    ),
                    unsafe_allow_html=True
                )

            st.write("")

            chart_col, details_col = st.columns(
                [1.1, 1],
                gap="medium"
            )

            # Attack distribution chart

            with chart_col:

                with st.container(border=True):

                    st.markdown("""
                    <div class="td-panel-title">Attack Category Distribution</div>
                    <div class="td-panel-subtitle">
                        Number of network flows classified under each known attack.
                    </div>
                    """, unsafe_allow_html=True)

                    fig = go.Figure(
                        data=[
                            go.Bar(
                                y=attack_counts.index.astype(str),
                                x=attack_counts.values,
                                orientation="h",
                                marker_color="#FF7777",
                                text=attack_counts.values,
                                textposition="outside",
                                cliponaxis=False
                            )
                        ]
                    )

                    fig.update_layout(
                        height=max(
                            340,
                            min(620, 48 * len(attack_counts) + 120)
                        ),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(
                            color="#A8B8CB",
                            size=14
                        ),
                        margin=dict(
                            l=8,
                            r=45,
                            t=15,
                            b=35
                        ),
                        showlegend=False,
                        xaxis=dict(
                            showgrid=True,
                            gridcolor="rgba(148,163,184,0.12)",
                            title="Number of Flows",
                            rangemode="tozero",
                            automargin=True
                        ),
                        yaxis=dict(
                            showgrid=False,
                            title="Attack Type",
                            autorange="reversed",
                            automargin=True
                        )
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        config={"displayModeBar": False}
                    )

            # Attack category summary

            with details_col:

                with st.container(border=True):

                    st.markdown("""
                    <div class="td-panel-title">Detected Attack Types</div>
                    <div class="td-panel-subtitle">
                        Detailed breakdown of identified threat categories.
                    </div>
                    """, unsafe_allow_html=True)

                    attack_table = (
                        attack_counts
                        .rename_axis("Attack Type")
                        .reset_index(name="Number of Flows")
                    )

                    st.dataframe(
                        attack_table,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.write("")

                    st.markdown(
                        '<div class="td-chip">RANDOM FOREST CLASSIFICATION</div>',
                        unsafe_allow_html=True
                    )

                    st.caption(
                        "Random Forest identifies known attack categories "
                        "based on patterns learned from its training data."
                    )

            st.write("")

            # Attack records and filtering

            with st.container(border=True):

                st.markdown("""
                <div class="td-section-kicker">INVESTIGATION CONSOLE</div>
                <div class="td-panel-title">Attack Records</div>
                <div class="td-panel-subtitle">
                    Filter and inspect individual records classified as known attacks.
                </div>
                """, unsafe_allow_html=True)

                attack_options = ["All Attack Types"] + sorted(
                    attack_predictions.astype(str).unique().tolist()
                )

                selected_attack = st.selectbox(
                    "Filter by attack category",
                    attack_options
                )

                if selected_attack == "All Attack Types":
                    selected_attack_mask = known_attack_mask
                else:
                    selected_attack_mask = (
                        known_attack_mask
                        & (analysis_df["RF Prediction"] == selected_attack)
                    )

                filtered_attack_count = int(selected_attack_mask.sum())
                filtered_attacks = analysis_df.loc[selected_attack_mask]

                st.markdown(
                    f"""
                    <div class="td-record-count">
                        <b>{len(filtered_attacks):,}</b> matching attack records
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.dataframe(
                    filtered_attacks.head(200),
                    use_container_width=True,
                    hide_index=True
                )

                if len(filtered_attacks) > 200:

                    st.caption(
                        "Showing the first 200 records. "
                        "Download the report to access all matching records."
                    )

                st.download_button(
                    "⬇️ Download Threat Report",
                    data=lambda: filtered_attacks.to_csv(index=False).encode("utf-8"),
                    file_name="sentinel_ai_threat_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
