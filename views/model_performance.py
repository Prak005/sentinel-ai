
"""Offline model evaluation and architecture page."""

from html import escape

import streamlit as st
import pandas as pd

from ui.components import page_header


MODEL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ===== MODEL PERFORMANCE ===== */

.mp-intro {
    background: linear-gradient(115deg, rgba(20,37,59,0.95), rgba(13,25,43,0.95));
    border: 1px solid rgba(87,230,224,0.18);
    border-radius: 16px;
    padding: 25px 28px;
    margin: 12px 0 22px 0;
}

.mp-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 9px;
    font-family: 'Rajdhani', sans-serif;
}

.mp-intro-title {
    color: #F1F6FF;
    font-size: 30px;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.mp-intro-copy {
    color: #A8B8CB;
    font-size: 17px;
    line-height: 1.7;
    margin: 0;
    font-family: 'Rajdhani', sans-serif;
}

.mp-info-banner {
    background: rgba(87,230,224,0.055);
    border: 1px solid rgba(87,230,224,0.20);
    border-left: 4px solid #57E6E0;
    border-radius: 10px;
    padding: 15px 19px;
    color: #B8C9DB;
    font-size: 16px;
    line-height: 1.7;
    font-family: 'Rajdhani', sans-serif;
    margin-bottom: 26px;
}

/* Section headings */

.mp-section {
    margin: 27px 0 16px 0;
}

.mp-section-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-bottom: 5px;
    font-family: 'Rajdhani', sans-serif;
}

.mp-section-title {
    color: #F1F6FF;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.4;
    font-family: 'Orbitron', sans-serif;
}

.mp-section-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.6;
    margin-top: 4px;
    font-family: 'Rajdhani', sans-serif;
}

/* Metric cards */

.mp-metric-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid rgba(148,163,184,0.15);
    border-left: 4px solid var(--mp-accent);
    border-radius: 13px;
    padding: 19px 17px;
    min-height: 133px;
}

.mp-metric-label {
    color: #A8B8CB;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
    font-family: 'Rajdhani', sans-serif;
}

.mp-metric-value {
    color: #F1F6FF;
    font-size: 29px;
    font-weight: 800;
    line-height: 1.25;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.mp-metric-note {
    color: #879AB1;
    font-size: 14px;
    line-height: 1.5;
    font-family: 'Rajdhani', sans-serif;
}

/* Architecture cards */

.mp-model-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid rgba(148,163,184,0.16);
    border-top: 3px solid var(--mp-accent);
    border-radius: 14px;
    padding: 21px;
    height: 100%;
}

.mp-model-title {
    color: #F1F6FF;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 7px;
    font-family: 'Orbitron', sans-serif;
}

.mp-model-subtitle {
    color: #93A6BC;
    font-size: 15px;
    margin-bottom: 17px;
    font-family: 'Rajdhani', sans-serif;
}

.mp-detail-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    padding: 11px 0;
    border-bottom: 1px solid rgba(148,163,184,0.10);
    font-family: 'Rajdhani', sans-serif;
}

.mp-detail-row:last-child {
    border-bottom: none;
}

.mp-detail-label {
    color: #91A5BC;
    font-size: 15px;
}

.mp-detail-value {
    color: #E7F0FC;
    font-size: 15px;
    font-weight: 700;
    text-align: right;
}

/* Hybrid rules */

.mp-rule-card {
    background: #111E30;
    border: 1px solid rgba(148,163,184,0.15);
    border-radius: 11px;
    padding: 17px;
    height: 100%;
}

.mp-rule-condition {
    color: #A8B8CB;
    font-size: 15px;
    line-height: 1.7;
    font-family: 'Rajdhani', sans-serif;
}

.mp-rule-result {
    color: #57E6E0;
    font-size: 17px;
    font-weight: 700;
    margin-top: 9px;
    font-family: 'Orbitron', sans-serif;
}

/* Notes */

.mp-note {
    background: rgba(255,184,107,0.055);
    border-left: 3px solid #FFB86B;
    border-radius: 8px;
    padding: 15px 18px;
    color: #B9C5D5;
    font-size: 16px;
    line-height: 1.7;
    font-family: 'Rajdhani', sans-serif;
    margin: 16px 0;
}

.mp-method-box {
    background: rgba(87,230,224,0.045);
    border: 1px solid rgba(87,230,224,0.14);
    border-radius: 12px;
    padding: 17px;
    min-height: 105px;
}

.mp-method-value {
    color: #F1F6FF;
    font-size: 25px;
    font-weight: 700;
    font-family: 'Orbitron', sans-serif;
}

.mp-method-label {
    color: #A8B8CB;
    font-size: 15px;
    margin-top: 7px;
    font-family: 'Rajdhani', sans-serif;
}

/* Consistent typography */

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

</style>
"""


def section_heading(kicker, title, subtitle):
    return (
        '<div class="mp-section">'
        f'<div class="mp-section-kicker">{escape(kicker)}</div>'
        f'<div class="mp-section-title">{escape(title)}</div>'
        f'<div class="mp-section-copy">{escape(subtitle)}</div>'
        '</div>'
    )


def metric_card(label, value, note, accent="#57E6E0"):
    return (
        f'<div class="mp-metric-card" style="--mp-accent:{accent}">'
        f'<div class="mp-metric-label">{escape(label)}</div>'
        f'<div class="mp-metric-value">{escape(str(value))}</div>'
        f'<div class="mp-metric-note">{escape(note)}</div>'
        '</div>'
    )


def architecture_card(title, subtitle, accent, details):

    rows = "".join(
        '<div class="mp-detail-row">'
        f'<span class="mp-detail-label">{escape(label)}</span>'
        f'<span class="mp-detail-value">{escape(value)}</span>'
        '</div>'
        for label, value in details
    )

    return (
        f'<div class="mp-model-card" style="--mp-accent:{accent}">'
        f'<div class="mp-model-title">{escape(title)}</div>'
        f'<div class="mp-model-subtitle">{escape(subtitle)}</div>'
        f'{rows}'
        '</div>'
    )


def render_metric_cards(metrics, accent="#57E6E0"):

    columns = st.columns(len(metrics), gap="small")

    for column, (label, value, note) in zip(columns, metrics):

        with column:
            st.markdown(
                metric_card(label, value, note, accent),
                unsafe_allow_html=True
            )


def render_page():

    st.markdown(MODEL_CSS, unsafe_allow_html=True)

    page_header(
        "Model Performance",
        "Evaluate the performance and architecture of Sentinel AI's hybrid detection system."
    )

    # Introduction

    st.markdown(
        '<div class="mp-intro">'
        '<div class="mp-kicker">SYSTEM INTELLIGENCE / MODEL EVALUATION</div>'
        '<div class="mp-intro-title">Model Performance Analytics</div>'
        '<p class="mp-intro-copy">'
        'Evaluate the detection capabilities of Random Forest, '
        'Isolation Forest and the Hybrid Detection system using '
        'the CIC-IDS2017 benchmark dataset.'
        '</p></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="mp-info-banner">'
        '<b>OFFLINE DATASET EVALUATION</b><br>'
        'Models were evaluated on 564,743 unseen network traffic records. '
        'These are offline benchmark results, not live network monitoring results.'
        '</div>',
        unsafe_allow_html=True
    )

    # Random Forest multiclass results

    st.markdown(
        section_heading(
            "MODEL 01 / SUPERVISED LEARNING",
            "Random Forest Performance",
            "Multiclass classification results across known network traffic categories."
        ),
        unsafe_allow_html=True
    )

    render_metric_cards([
        ("Accuracy", "93.68%", "Overall correct predictions"),
        ("Weighted Precision", "96.84%", "Precision weighted by class support"),
        ("Weighted Recall", "95.68%", "Recall weighted by class support"),
        ("Weighted F1", "95.74%", "Weighted harmonic mean"),
        ("Macro F1", "81.34%", "Equal importance to each class")
    ])

    st.caption(
        "Macro F1 gives equal importance to every attack class, "
        "while weighted metrics account for class frequency."
    )

    st.divider()

    # Model comparison

    st.markdown(
        section_heading(
            "MODEL COMPARISON / BINARY CLASSIFICATION",
            "Binary Attack Detection Performance",
            "Comparison of BENIGN versus ATTACK classification across all three approaches."
        ),
        unsafe_allow_html=True
    )

    comparison_df = pd.DataFrame([
        {
            "Model": "Random Forest",
            "Accuracy": "93.68%",
            "Precision": "96.84%",
            "Recall": "95.68%",
            "F1 Score": "95.74%",
            "False Positive Rate": "0.33%"
        },
        {
            "Model": "Isolation Forest",
            "Accuracy": "82.88%",
            "Precision": "58.21%",
            "Recall": "43.65%",
            "F1 Score": "49.89%",
            "False Positive Rate": "7.60%"
        },
        {
            "Model": "Hybrid Detection",
            "Accuracy": "93.60%",
            "Precision": "75.35%",
            "Recall": "95.89%",
            "F1 Score": "85.90%",
            "False Positive Rate": "7.93%"
        }
    ])

    with st.container(border=True):

        st.markdown(
            '<div class="mp-panel-title">Model Comparison Matrix</div>'
            '<div class="mp-panel-subtitle">'
            'Performance metrics across the three detection approaches.'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # Hybrid model analysis

    st.markdown(
        section_heading(
            "MODEL 03 / COMBINED INTELLIGENCE",
            "Hybrid Detection Analysis",
            "Combining supervised classification with unsupervised anomaly detection."
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="mp-intro-copy" style="margin-bottom:18px">'
        'Sentinel AI combines Random Forest and Isolation Forest '
        'to identify known attacks as well as unusual traffic patterns.'
        '</div>',
        unsafe_allow_html=True
    )

    render_metric_cards([
        ("Attack Detection Recall", "95.89%", "Actual attacks detected"),
        ("Precision", "75.35%", "Predicted attacks correctly identified"),
        ("F1 Score", "85.90%", "Precision-recall balance"),
        ("False Positive Rate", "7.93%", "Benign traffic flagged incorrectly")
    ], accent="#FFB86B")

    st.markdown(
        '<div class="mp-note">'
        '<b>DETECTION TRADE-OFF:</b> Hybrid detection achieves high recall '
        'but also produces more false positives. Compared with binary '
        'Random Forest, it catches 8 additional attack records '
        '(123 instead of 131 missed attacks), but produces 34,555 '
        'additional false positives. Suspicious Anomaly should therefore '
        'be treated as a review alert, not a confirmed attack.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # Model architecture

    st.markdown(
        section_heading(
            "SYSTEM DESIGN / MODEL ARCHITECTURE",
            "Model Architecture",
            "Two complementary machine learning models power the detection pipeline."
        ),
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:

        st.markdown(
            architecture_card(
                "Random Forest",
                "Supervised classification engine",
                "#57E6E0",
                [
                    ("Learning Type", "Supervised Learning"),
                    ("Training Data", "Stratified CIC-IDS2017 sample"),
                    ("Training Samples", "500,450"),
                    ("Input Features", "78 network-flow features"),
                    ("Primary Purpose", "Classify known attacks"),
                    ("Output", "BENIGN + 14 attack categories")
                ]
            ),
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            architecture_card(
                "Isolation Forest",
                "Unsupervised anomaly detection engine",
                "#FFB86B",
                [
                    ("Learning Type", "Unsupervised Learning"),
                    ("Training Data", "BENIGN traffic only"),
                    ("Training Samples", "100,000"),
                    ("Input Features", "78 network-flow features"),
                    ("Primary Purpose", "Identify unusual traffic"),
                    ("Output", "Normal or Anomaly")
                ]
            ),
            unsafe_allow_html=True
        )

    st.divider()

    # Hybrid detection strategy

    st.markdown(
        section_heading(
            "DECISION ENGINE / HYBRID LOGIC",
            "Hybrid Detection Strategy",
            "The final classification is determined by combining both model outputs."
        ),
        unsafe_allow_html=True
    )

    rule_col1, rule_col2, rule_col3 = st.columns(3, gap="medium")

    rules = [
        (
            "RULE 01",
            "Random Forest: Attack",
            "Isolation Forest: Any result",
            "KNOWN ATTACK",
            "#FF7777"
        ),
        (
            "RULE 02",
            "Random Forest: BENIGN",
            "Isolation Forest: Anomaly",
            "SUSPICIOUS ANOMALY",
            "#FFB86B"
        ),
        (
            "RULE 03",
            "Random Forest: BENIGN",
            "Isolation Forest: Normal",
            "NORMAL",
            "#45D6C2"
        )
    ]

    for column, rule in zip(
        [rule_col1, rule_col2, rule_col3],
        rules
    ):

        label, condition1, condition2, result, accent = rule

        with column:

            st.markdown(
                f'<div class="mp-rule-card" style="border-top:3px solid {accent}">'
                f'<div class="mp-section-kicker">{label}</div>'
                f'<div class="mp-rule-condition">{condition1}<br>{condition2}</div>'
                f'<div class="mp-rule-result" style="color:{accent}">{result}</div>'
                '</div>',
                unsafe_allow_html=True
            )

    st.divider()

    # Evaluation methodology

    st.markdown(
        section_heading(
            "BENCHMARK / EVALUATION",
            "Evaluation Methodology",
            "Dataset preparation and validation details used for offline evaluation."
        ),
        unsafe_allow_html=True
    )

    method_col1, method_col2, method_col3, method_col4 = st.columns(4)

    method_metrics = [
        ("2,823,723", "Processed Records"),
        ("2,258,980", "Training Records"),
        ("564,743", "Testing Records"),
        ("ZERO", "Overlapping Feature Groups")
    ]

    for column, (value, label) in zip(
        [method_col1, method_col2, method_col3, method_col4],
        method_metrics
    ):

        with column:

            st.markdown(
                '<div class="mp-method-box">'
                f'<div class="mp-method-value">{value}</div>'
                f'<div class="mp-method-label">{label}</div>'
                '</div>',
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="mp-panel-title" style="margin-top:24px">'
        'Understanding Evaluation Metrics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        - **Accuracy:** Overall proportion of correct predictions.
        - **Precision:** Proportion of predicted attacks that were actual attacks.
        - **Recall:** Proportion of actual attacks successfully detected.
        - **F1 Score:** Harmonic mean of precision and recall.
        - **False Positive Rate:** Proportion of benign traffic incorrectly flagged.
        - **Confusion Matrix:** Shows true positives, true negatives,
          false positives and false negatives.
        """
    )

    st.markdown(
        '<div class="mp-note">'
        '<b>DATASET LIMITATION:</b> CIC-IDS2017 has a highly imbalanced '
        'class distribution. Performance on extremely rare categories '
        'such as Heartbleed and SQL Injection should be interpreted cautiously.'
        '</div>',
        unsafe_allow_html=True
    )
