
"""Traffic Analyzer page for Sentinel AI."""

import hashlib
import logging
from html import escape

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.inference import predict_traffic
from src.csv_io import read_traffic_csv
from ui.components import page_header

logger = logging.getLogger(__name__)


# =========================================================
# SENTINEL AI - TRAFFIC ANALYZER THEME
# =========================================================

TRAFFIC_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700&family=Rajdhani:wght@500;600;700&display=swap');

.ta-intro {
    padding: 20px 23px;
    border: 1px solid #28505e;
    border-radius: 15px;
    background:
        radial-gradient(circle at 90% 0%, #16404a 0, transparent 38%),
        linear-gradient(120deg, #10283a, #0b192a);
    margin: 8px 0 16px;
}

.ta-kicker {
    color: #63d7ca;
    font: 700 10px 'Rajdhani';
    letter-spacing: 1.8px;
}

.ta-heading {
    color: #eff7fc;
    font: 700 21px 'Orbitron';
    margin-top: 8px;
}

.ta-heading span {
    color: #5ce0d1;
}

.ta-description {
    color: #91a9bb;
    font-size: 12px;
    margin-top: 7px;
    line-height: 1.6;
}

.ta-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin: 22px 0 12px;
}

.ta-section small {
    color: #63c9c1;
    font: 700 10px 'Rajdhani';
    letter-spacing: 1.6px;
}

.ta-section h3 {
    color: #eaf2f8;
    font: 600 16px 'Orbitron';
    margin: 5px 0;
}

.ta-section p {
    color: #839bad;
    font-size: 11px;
    margin: 0;
}

.ta-chip {
    color: #71d4cb;
    border: 1px solid #397d78;
    border-radius: 20px;
    padding: 6px 10px;
    font: 700 9px 'Rajdhani';
    letter-spacing: 1px;
    white-space: nowrap;
}

.ta-upload-heading {
    color: #65d7cc;
    font: 700 10px 'Rajdhani';
    letter-spacing: 1.5px;
}

.ta-upload-title {
    color: #e9f2f9;
    font: 600 16px 'Orbitron';
    margin-top: 5px;
}

.ta-upload-sub {
    color: #8ba3b5;
    font-size: 11px;
    margin-top: 5px;
}

[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(135deg, #10283a, #101e30) !important;
    border: 1px dashed #398d8b !important;
    border-radius: 13px !important;
    padding: 22px 12px !important;
}

[data-testid="stFileUploaderDropzone"]:hover {
    border-color: #5ce0d1 !important;
    background: #142d40 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #c0d2df !important;
}

.ta-file-strip {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
    background: #10283a;
    border: 1px solid #2b5363;
    border-radius: 10px;
    padding: 12px 15px;
    margin: 12px 0;
}

.ta-file-name {
    color: #e6f4f7;
    font: 600 13px 'Rajdhani';
    overflow-wrap: anywhere;
}

.ta-file-meta {
    color: #8ba8b8;
    font: 600 10px 'Rajdhani';
    letter-spacing: .7px;
}

.ta-metric {
    position: relative;
    overflow: hidden;
    padding: 15px 16px;
    min-height: 116px;
    border: 1px solid #ffffff1c;
    border-radius: 13px;
    background: linear-gradient(145deg, #142b40, #0c1b2c);
}

.ta-metric:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: var(--accent);
}

.ta-metric-label {
    color: #9fb5c5;
    font: 700 10px 'Rajdhani';
    letter-spacing: 1px;
}

.ta-metric-value {
    color: #f1f6fb;
    font: 700 23px 'Orbitron';
    margin-top: 10px;
}

.ta-metric-note {
    color: #7891a4;
    font-size: 10px;
    margin-top: 5px;
}

.ta-panel-title {
    color: #65c8c0;
    font: 700 10px 'Rajdhani';
    letter-spacing: 1.4px;
}

.ta-panel-title b {
    display: block;
    color: #e8f0f7;
    font: 600 14px 'Orbitron';
    letter-spacing: 0;
    margin-top: 5px;
}

.ta-panel-title span {
    display: block;
    color: #8199aa;
    font: 400 11px sans-serif;
    margin-top: 5px;
}

.ta-result-banner {
    padding: 14px 17px;
    border: 1px solid #2c7168;
    border-radius: 11px;
    background: linear-gradient(100deg, #123c3b, #102a38);
    margin: 15px 0;
}

.ta-result-banner strong {
    color: #8af0d9;
    font: 700 13px 'Rajdhani';
    letter-spacing: 1px;
}

.ta-result-banner span {
    display: block;
    color: #a4c7c8;
    font-size: 10px;
    margin-top: 4px;
}

.ta-empty {
    padding: 24px 12px;
    text-align: center;
    color: #dce8f1;
}

.ta-empty b {
    display: block;
    font: 700 15px 'Rajdhani';
    margin-top: 8px;
}

.ta-empty span {
    display: block;
    color: #8299aa;
    font-size: 11px;
    margin-top: 5px;
}

.ta-table-note {
    color: #8da4b5;
    font-size: 11px;
    margin: 7px 0 12px;
}

.ta-download-label {
    color: #63d4c8;
    font: 700 10px 'Rajdhani';
    letter-spacing: 1.5px;
}

@media(max-width: 750px) {
    .ta-section {
        align-items: flex-start;
        flex-direction: column;
    }

    .ta-intro {
        padding: 17px;
    }
}
/* ===== READABLE FONT SIZE OVERRIDE ===== */

/* General page text */
.main .stMarkdown p,
.main .stMarkdown li,
.main label,
.main [data-testid="stCaptionContainer"] {
    font-size: 16px !important;
    line-height: 1.65 !important;
}

/* Main headings */
.main .ta-heading {
    font-size: 32px !important;
    line-height: 1.25 !important;
}

.main .ta-section {
    font-size: 25px !important;
    line-height: 1.35 !important;
}

.main .ta-kicker {
    font-size: 13px !important;
}

/* Intro and descriptions */
.main .ta-intro {
    font-size: 18px !important;
    line-height: 1.7 !important;
}

.main .ta-panel-title {
    font-size: 23px !important;
    line-height: 1.4 !important;
}

.main .ta-upload-heading {
    font-size: 22px !important;
}

.main .ta-result-banner,
.main .ta-empty {
    font-size: 17px !important;
    line-height: 1.6 !important;
}

/* Metric cards */
.main .ta-metric {
    font-size: 16px !important;
}

.main .ta-metric b,
.main .ta-metric strong {
    font-size: 30px !important;
}

.main .ta-chip {
    font-size: 14px !important;
}

/* File information and notes */
.main .ta-file-strip {
    font-size: 16px !important;
}

.main .ta-table-note,
.main .ta-download-label {
    font-size: 15px !important;
}

/* Upload area and buttons */
.main [data-testid="stFileUploader"] * {
    font-size: 16px !important;
}

.main .stButton button {
    font-size: 17px !important;
    min-height: 48px !important;
}

/* Native Streamlit metrics */
.main [data-testid="stMetricLabel"] {
    font-size: 15px !important;
}

.main [data-testid="stMetricValue"] {
    font-size: 29px !important;
}

/* Tables */
.main [data-testid="stDataFrame"] {
    font-size: 15px !important;
}

/* Plotly chart labels */
.main .js-plotly-plot .xtick text,
.main .js-plotly-plot .ytick text {
    font-size: 14px !important;
}
</style>
"""


# =========================================================
# REUSABLE UI HELPERS
# =========================================================

def metric_card(label, value, note, accent):
    st.markdown(
        f"""
        <div class="ta-metric" style="--accent:{accent}">
            <div class="ta-metric-label">{label}</div>
            <div class="ta-metric-value">{value:,}</div>
            <div class="ta-metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_heading(kicker, title, subtitle, chip=None):
    chip_html = (
        f'<div class="ta-chip">{chip}</div>'
        if chip else ""
    )

    st.markdown(
        f"""
        <div class="ta-section">
            <div>
                <small>{kicker}</small>
                <h3>{title}</h3>
                <p>{subtitle}</p>
            </div>
            {chip_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def panel_heading(kicker, title, subtitle):
    st.markdown(
        f"""
        <div class="ta-panel-title">
            {kicker}
            <b>{title}</b>
            <span>{subtitle}</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# MAIN PAGE
# =========================================================

def render_page():

    st.markdown(TRAFFIC_CSS, unsafe_allow_html=True)

    page_header(
        "Traffic Analyzer",
        "Upload network-flow CSV files and detect malicious traffic using hybrid ML."
    )

    # INTRODUCTION
    st.markdown(
        """
        <div class="ta-intro">
            <div class="ta-kicker">SENTINEL AI / TRAFFIC INTELLIGENCE</div>
            <div class="ta-heading">
                Network <span>Traffic Analyzer</span>
            </div>
            <div class="ta-description">
                Inspect network-flow datasets, classify known attacks
                and identify suspicious traffic through hybrid machine learning.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CSV UPLOAD
    # =====================================================

    with st.container(border=True):

        st.markdown(
            """
            <div class="ta-upload-heading">01 / DATASET INGESTION</div>
            <div class="ta-upload-title">Upload Network Traffic</div>
            <div class="ta-upload-sub">
                Import a compatible network-flow CSV dataset for analysis.
                Maximum upload size: 200 MB.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        uploaded_file = st.file_uploader(
            "Choose a network traffic CSV file",
            type=["csv"],
            max_upload_size=200,
            key="traffic_csv_upload"
        )

        if uploaded_file is not None:

            try:
                # Hash the existing upload buffer without creating another
                # 75-200 MB bytes object via getvalue().
                file_digest = hashlib.sha256(
                    uploaded_file.getbuffer()
                ).hexdigest()
                uploaded_file.seek(0)

                current_file = (
                    uploaded_file.name,
                    uploaded_file.size,
                    file_digest
                )

                cached_file = st.session_state.get("sentinel_upload_file")

                if cached_file == current_file:
                    # Reuse the DataFrame across Streamlit reruns. Re-reading
                    # the CSV while the previous analysis remains in session
                    # state would temporarily double its memory footprint.
                    df = st.session_state.get("sentinel_analysis_df")
                    if df is None:
                        df = st.session_state.get("sentinel_upload_df")
                else:
                    # Release the previous dataset before parsing a new upload.
                    for key in (
                        "sentinel_analysis_df",
                        "sentinel_analysis_file",
                        "sentinel_upload_df",
                        "sentinel_upload_file",
                    ):
                        st.session_state.pop(key, None)
                    df = None

                if df is None:
                    df = read_traffic_csv(uploaded_file)
                    st.session_state["sentinel_upload_df"] = df
                    st.session_state["sentinel_upload_file"] = current_file

                # FILE INFORMATION
                st.markdown(
                    f"""
                    <div class="ta-file-strip">
                        <div>
                            <div class="ta-file-meta">SELECTED DATASET</div>
                            <div class="ta-file-name">
                                ◈ {escape(uploaded_file.name)}
                            </div>
                        </div>
                        <div class="ta-file-meta">
                            {uploaded_file.size / (1024 * 1024):.2f} MB
                            &nbsp; | &nbsp; CSV FILE
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # DATASET INFORMATION
                section_heading(
                    "DATASET INSPECTION",
                    "Dataset Overview",
                    "A quick look at the uploaded network-flow data.",
                    "FILE VALIDATED"
                )

                a, b, c = st.columns(3, gap="medium")

                with a:
                    metric_card(
                        "TOTAL RECORDS",
                        len(df),
                        "Network-flow entries",
                        "#58d8cf"
                    )

                raw_columns = [
                    column for column in df.columns
                    if column not in {
                        "RF Prediction", "IF Prediction", "Anomaly Score",
                        "Final Status", "Risk Level"
                    }
                ]
                missing_value_count = sum(
                    int(df[column].isna().sum()) for column in raw_columns
                )

                with b:
                    metric_card(
                        "TOTAL FEATURES",
                        len(raw_columns),
                        "Available dataset columns",
                        "#69b9ef"
                    )

                with c:
                    metric_card(
                        "MISSING VALUES",
                        missing_value_count,
                        "Empty data cells",
                        "#f4b95f"
                    )

                # DATASET PREVIEW
                section_heading(
                    "02 / DATA EXPLORATION",
                    "Dataset Preview",
                    "Review the first 20 records before running detection.",
                    "RAW DATA"
                )

                with st.container(border=True):

                    st.dataframe(
                        df.iloc[:20].loc[:, raw_columns],
                        use_container_width=True,
                        hide_index=True
                    )

                    st.caption(
                        f"Previewing 20 of {len(df):,} records "
                        f"and {len(df.columns):,} columns."
                    )

                st.write("")

                # =================================================
                # RUN HYBRID DETECTION
                # =================================================

                section_heading(
                    "03 / INTELLIGENCE ENGINE",
                    "Run Hybrid Detection",
                    "Random Forest classification + Isolation Forest anomaly detection.",
                    "RF + IF"
                )

                if st.button(
                    "🛡️ LET'S ANALYZE !!",
                    use_container_width=True,
                    type="primary"
                ):

                    try:
                        with st.spinner(
                            "Analyzing!! Just Hold on ...."
                        ):

                            results = predict_traffic(df)

                            # Attach prediction columns to the existing frame
                            # rather than concatenating and copying the full
                            # 75-200 MB source dataset.
                            for column in results.columns:
                                df[column] = results[column].to_numpy(copy=False)

                            del results

                            st.session_state["sentinel_analysis_df"] = df
                            st.session_state["sentinel_analysis_file"] = current_file
                            st.session_state.pop("sentinel_upload_df", None)

                        st.success(
                            "Traffic analysis completed successfully!"
                        )

                    except FileNotFoundError as e:
                        st.error(
                            f"Required model files are missing: {e}"
                        )

                    except ValueError as e:
                        st.error(
                            f"Dataset validation failed: {e}"
                        )

                    except Exception:
                        logger.exception(
                            "Unexpected failure during traffic inference"
                        )

                        st.error(
                            "Unable to analyze traffic because of an "
                            "unexpected internal error. "
                            "Check the terminal logs for details."
                        )

                # =================================================
                # DISPLAY RESULTS FOR CURRENT FILE ONLY
                # =================================================

                if (
                    st.session_state.get("sentinel_analysis_file")
                    == current_file
                    and "sentinel_analysis_df"
                    in st.session_state
                ):

                    analysis_df = st.session_state[
                        "sentinel_analysis_df"
                    ]

                    st.markdown(
                        """
                        <div class="ta-result-banner">
                            <strong>✓ HYBRID ANALYSIS COMPLETED</strong>
                            <span>
                                Traffic classification results are ready.
                                Review the detection summary and detailed report below.
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # DETECTION STATISTICS
                    section_heading(
                        "04 / DETECTION INTELLIGENCE",
                        "Hybrid Detection Results",
                        "Classification summary generated by the detection engine.",
                        "ANALYSIS OUTPUT"
                    )

                    known_attacks = int(
                        (
                            analysis_df["Final Status"]
                            == "Known Attack"
                        ).sum()
                    )

                    anomalies = int(
                        (
                            analysis_df["Final Status"]
                            == "Suspicious Anomaly"
                        ).sum()
                    )

                    normal = int(
                        (
                            analysis_df["Final Status"]
                            == "Normal"
                        ).sum()
                    )

                    total_flows = len(analysis_df)

                    m1, m2, m3, m4 = st.columns(4, gap="medium")

                    with m1:
                        metric_card(
                            "TOTAL FLOWS",
                            total_flows,
                            "Analyzed traffic records",
                            "#58d8cf"
                        )

                    with m2:
                        metric_card(
                            "KNOWN ATTACKS",
                            known_attacks,
                            "Identified attack labels",
                            "#ff7180"
                        )

                    with m3:
                        metric_card(
                            "SUSPICIOUS ANOMALIES",
                            anomalies,
                            "Unusual traffic patterns",
                            "#f4b95f"
                        )

                    with m4:
                        metric_card(
                            "NORMAL TRAFFIC",
                            normal,
                            "Classified as normal",
                            "#69d9a7"
                        )

                    # =================================================
                    # CHARTS AND ATTACK CATEGORIES
                    # =================================================

                    section_heading(
                        "05 / VISUAL ANALYTICS",
                        "Traffic Intelligence",
                        "Explore the classification distribution and detected attack categories."
                    )

                    chart_left, chart_right = st.columns(
                        [1.2, 1],
                        gap="medium"
                    )

                    with chart_left:

                        with st.container(border=True):

                            panel_heading(
                                "CLASSIFICATION OUTPUT",
                                "Detection Distribution",
                                "Hybrid model classification results."
                            )

                            categories = [
                                "Known Attack",
                                "Suspicious Anomaly",
                                "Normal"
                            ]

                            values = [
                                known_attacks,
                                anomalies,
                                normal
                            ]

                            fig = go.Figure(
                                data=[
                                    go.Bar(
                                        y=categories,
                                        x=values,
                                        orientation="h",
                                        marker=dict(
                                            color=[
                                                "#ff7180",
                                                "#f4b95f",
                                                "#58d8cf"
                                            ],
                                            line=dict(
                                                width=0
                                            )
                                        ),
                                        text=values,
                                        texttemplate="%{x:,.0f}",
                                        textposition="outside",
                                        cliponaxis=False
                                    )
                                ]
                            )

                            fig.update_layout(
                                height=320,
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                font=dict(
                                    color="#a8b8cb",
                                    family="Rajdhani",
                                    size=12
                                ),
                                margin=dict(
                                    l=8,
                                    r=35,
                                    t=20,
                                    b=8
                                ),
                                showlegend=False,
                                xaxis=dict(
                                    showgrid=True,
                                    gridcolor="rgba(148,163,184,0.10)",
                                    title="Number of Flows",
                                    rangemode="tozero"
                                ),
                                yaxis=dict(
                                    showgrid=False,
                                    autorange="reversed"
                                )
                            )

                            st.plotly_chart(
                                fig,
                                use_container_width=True,
                                config={"displayModeBar": False}
                            )

                    with chart_right:

                        with st.container(border=True):

                            panel_heading(
                                "ATTACK INTELLIGENCE",
                                "Known Attack Categories",
                                "Attack labels identified by Random Forest."
                            )

                            attack_data = (
                                analysis_df[
                                    analysis_df["Final Status"]
                                    == "Known Attack"
                                ]["RF Prediction"]
                                .value_counts()
                            )

                            if not attack_data.empty:

                                attack_table = (
                                    attack_data
                                    .rename_axis("Attack Type")
                                    .reset_index(name="Flows")
                                )

                                st.dataframe(
                                    attack_table,
                                    use_container_width=True,
                                    hide_index=True,
                                    height=320
                                )

                            else:

                                st.markdown(
                                    """
                                    <div class="ta-empty">
                                        <div style="font-size:25px;color:#69d9a7">✓</div>
                                        <b>No known attack categories detected</b>
                                        <span>
                                            Random Forest did not classify
                                            any flows as known attacks.
                                        </span>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                    # =================================================
                    # DETAILED ANALYSIS TABLE
                    # =================================================

                    section_heading(
                        "06 / FLOW-LEVEL INSPECTION",
                        "Detailed Traffic Analysis",
                        "Inspect model predictions, anomaly scores and final hybrid decisions.",
                        "FULL REPORT"
                    )

                    with st.container(border=True):

                        panel_heading(
                            "PREDICTION DETAILS",
                            "Traffic Classification Records",
                            "First 200 records from the analyzed dataset."
                        )

                        st.write("")

                        st.dataframe(
                            analysis_df.head(200),
                            use_container_width=True,
                            hide_index=True
                        )

                        if len(analysis_df) > 200:
                            st.markdown(
                                f"""
                                <div class="ta-table-note">
                                    Showing the first 200 records out of
                                    {len(analysis_df):,}.
                                    Download the complete report for all records.
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        st.divider()

                        st.markdown(
                            '<div class="ta-download-label">EXPORT ANALYSIS REPORT</div>',
                            unsafe_allow_html=True
                        )

                        st.write(
                            "Download the complete traffic analysis with all original features and prediction columns."
                        )

                        st.download_button(
                            label="⬇️  DOWNLOAD COMPLETE ANALYSIS REPORT",
                            data=lambda: analysis_df.to_csv(index=False).encode("utf-8"),
                            file_name="sentinel_ai_analysis.csv",
                            mime="text/csv",
                            use_container_width=True
                        )

            except ValueError as e:
                st.error(
                    f"Unable to read CSV file: {e}"
                )

            except Exception:
                logger.exception(
                    "Unexpected failure while reading uploaded CSV"
                )

                st.error(
                    "Unable to read this file. Ensure it is a valid CSV "
                    "and check the terminal logs if the problem continues."
                )

        else:

            st.markdown(
                """
                <div class="ta-empty">
                    <div style="font-size:30px;color:#5ce0d1">⇧</div>
                    <b>Awaiting Network Traffic Dataset</b>
                    <span>
                        Upload a compatible CSV file above to preview
                        network traffic and start hybrid intrusion detection.
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                "Upload a CSV file to preview network traffic records "
                "and run hybrid intrusion detection."
            )
