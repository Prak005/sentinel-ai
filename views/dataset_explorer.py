
"""Dataset exploration page for analyzed traffic data."""

from html import escape

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from ui.components import page_header


DATASET_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ===== DATASET EXPLORER ===== */

.de-intro {
    background: linear-gradient(115deg, rgba(20,37,59,0.95), rgba(13,25,43,0.95));
    border: 1px solid rgba(87,230,224,0.18);
    border-radius: 16px;
    padding: 25px 28px;
    margin: 12px 0 28px 0;
}

.de-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 9px;
    font-family: 'Rajdhani', sans-serif;
}

.de-intro-title {
    color: #F1F6FF;
    font-size: 30px;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.de-intro-copy {
    color: #A8B8CB;
    font-size: 17px;
    line-height: 1.7;
    margin: 0;
    font-family: 'Rajdhani', sans-serif;
}

/* Section headings */

.de-section {
    margin: 27px 0 16px 0;
}

.de-section-kicker {
    color: #57E6E0;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.8px;
    margin-bottom: 5px;
    font-family: 'Rajdhani', sans-serif;
}

.de-section-title {
    color: #F1F6FF;
    font-size: 26px;
    font-weight: 700;
    line-height: 1.4;
    font-family: 'Orbitron', sans-serif;
}

.de-section-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.6;
    margin-top: 4px;
    font-family: 'Rajdhani', sans-serif;
}

/* Metric cards */

.de-metric-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid rgba(148,163,184,0.15);
    border-left: 4px solid var(--de-accent);
    border-radius: 13px;
    padding: 20px 17px;
    min-height: 135px;
}

.de-metric-label {
    color: #A8B8CB;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 12px;
    font-family: 'Rajdhani', sans-serif;
}

.de-metric-value {
    color: #F1F6FF;
    font-size: 29px;
    font-weight: 800;
    line-height: 1.25;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.de-metric-note {
    color: #879AB1;
    font-size: 14px;
    line-height: 1.5;
    font-family: 'Rajdhani', sans-serif;
}

/* Panels */

.de-panel-title {
    color: #F1F6FF;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 5px;
    font-family: 'Orbitron', sans-serif;
}

.de-panel-subtitle {
    color: #93A6BC;
    font-size: 15px;
    line-height: 1.6;
    margin-bottom: 15px;
    font-family: 'Rajdhani', sans-serif;
}

.de-chip {
    display: inline-block;
    background: rgba(87,230,224,0.09);
    color: #57E6E0;
    border: 1px solid rgba(87,230,224,0.24);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
    margin-bottom: 12px;
    font-family: 'Rajdhani', sans-serif;
}

/* Empty state */

.de-empty {
    background: rgba(87,230,224,0.05);
    border: 1px solid rgba(87,230,224,0.20);
    border-radius: 14px;
    padding: 24px;
    margin: 20px 0;
}

.de-empty-title {
    color: #EAF3FF;
    font-size: 21px;
    font-weight: 700;
    margin-bottom: 8px;
    font-family: 'Orbitron', sans-serif;
}

.de-empty-copy {
    color: #A8B8CB;
    font-size: 16px;
    line-height: 1.7;
    font-family: 'Rajdhani', sans-serif;
}

/* Feature information */

.de-feature-info {
    background: rgba(87,230,224,0.045);
    border: 1px solid rgba(87,230,224,0.15);
    border-radius: 11px;
    padding: 16px 18px;
    margin-bottom: 16px;
    color: #B8C9DB;
    font-size: 16px;
    line-height: 1.7;
    font-family: 'Rajdhani', sans-serif;
}

/* Typography consistency */

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

.main div[data-baseweb="select"] * {
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

.main .js-plotly-plot .xtick text,
.main .js-plotly-plot .ytick text,
.main .js-plotly-plot .legend text {
    font-size: 14px !important;
    font-family: 'Rajdhani', sans-serif !important;
}

</style>
"""


def section_heading(kicker, title, subtitle):

    return (
        '<div class="de-section">'
        f'<div class="de-section-kicker">{escape(kicker)}</div>'
        f'<div class="de-section-title">{escape(title)}</div>'
        f'<div class="de-section-copy">{escape(subtitle)}</div>'
        '</div>'
    )


def metric_card(label, value, note, accent):

    return (
        f'<div class="de-metric-card" style="--de-accent:{accent}">'
        f'<div class="de-metric-label">{escape(label)}</div>'
        f'<div class="de-metric-value">{escape(str(value))}</div>'
        f'<div class="de-metric-note">{escape(note)}</div>'
        '</div>'
    )


def render_distribution_chart(labels, values, title):

    chart_height = max(340, min(620, len(labels) * 36 + 110))

    fig = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                marker_color="#57E6E0",
                text=values,
                textposition="outside",
                cliponaxis=False
            )
        ]
    )

    fig.update_layout(
        height=chart_height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Rajdhani, sans-serif",
            color="#A8B8CB",
            size=14
        ),
        margin=dict(l=10, r=45, t=15, b=35),
        showlegend=False,
        xaxis=dict(
            title=title,
            showgrid=True,
            gridcolor="rgba(148,163,184,0.12)",
            rangemode="tozero",
            automargin=True
        ),
        yaxis=dict(
            showgrid=False,
            autorange="reversed",
            automargin=True
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def render_page():

    st.markdown(DATASET_CSS, unsafe_allow_html=True)

    page_header(
        "Dataset Explorer",
        "Explore the structure and characteristics of your uploaded traffic dataset."
    )

    st.markdown(
        '<div class="de-intro">'
        '<div class="de-kicker">DATA INTELLIGENCE / DATASET ANALYSIS</div>'
        '<div class="de-intro-title">Network Dataset Explorer</div>'
        '<p class="de-intro-copy">'
        'Inspect network-flow records, understand feature structures, '
        'examine traffic labels and explore individual feature distributions.'
        '</p></div>',
        unsafe_allow_html=True
    )

    analysis_df = st.session_state.get("sentinel_analysis_df")

    if analysis_df is None or analysis_df.empty:

        st.markdown(
            '<div class="de-empty">'
            '<div class="de-empty-title">No Dataset Available</div>'
            '<div class="de-empty-copy">'
            'Upload and analyze a network-flow CSV in Traffic Analyzer '
            'to explore its records, features, schema and traffic distribution.'
            '</div></div>',
            unsafe_allow_html=True
        )

        st.info(
            "Your dataset information will appear here after traffic analysis."
        )

    else:

        # Remove model output columns to show the original dataset

        dataset_df = analysis_df.drop(
            columns=[
                "RF Prediction",
                "IF Prediction",
                "Anomaly Score",
                "Final Status"
            ],
            errors="ignore"
        ).copy()

        total_records = len(dataset_df)

        total_features = len([
            col for col in dataset_df.columns if col != "Label"
        ])

        missing_values = int(dataset_df.isna().sum().sum())

        duplicate_records = int(dataset_df.duplicated().sum())

        # Dataset overview

        st.markdown(
            section_heading(
                "DATASET OVERVIEW",
                "Dataset Health & Statistics",
                "A quick overview of the uploaded network traffic dataset."
            ),
            unsafe_allow_html=True
        )

        metric_columns = st.columns(4, gap="medium")

        metrics = [
            (
                "Total Records",
                f"{total_records:,}",
                "Network-flow observations",
                "#57E6E0"
            ),
            (
                "Total Features",
                f"{total_features:,}",
                "Input columns excluding Label",
                "#7C9CFF"
            ),
            (
                "Missing Values",
                f"{missing_values:,}",
                "Total missing data points",
                "#FFB86B"
            ),
            (
                "Duplicate Records",
                f"{duplicate_records:,}",
                "Repeated complete rows",
                "#FF7777"
            )
        ]

        for column, metric in zip(metric_columns, metrics):

            label, value, note, accent = metric

            with column:

                st.markdown(
                    metric_card(label, value, note, accent),
                    unsafe_allow_html=True
                )

        st.divider()

        # Dataset preview

        st.markdown(
            section_heading(
                "RECORD INSPECTION",
                "Dataset Preview",
                "Inspect the first 100 records from the uploaded dataset."
            ),
            unsafe_allow_html=True
        )

        with st.container(border=True):

            st.markdown(
                '<div class="de-chip">RAW NETWORK FLOW DATA</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                dataset_df.head(100),
                use_container_width=True
            )

            st.caption(
                f"Displaying {min(100, total_records):,} of "
                f"{total_records:,} total records."
            )

        st.divider()

        # Dataset schema

        st.markdown(
            section_heading(
                "FEATURE INTELLIGENCE",
                "Dataset Schema",
                "Explore column data types, missing values and unique values."
            ),
            unsafe_allow_html=True
        )

        schema_df = pd.DataFrame({
            "Column": dataset_df.columns.astype(str),
            "Data Type": [str(dtype) for dtype in dataset_df.dtypes],
            "Missing Values": dataset_df.isna().sum().values,
            "Unique Values": dataset_df.nunique().values
        })

        with st.container(border=True):

            st.markdown(
                '<div class="de-panel-title">Feature Structure</div>'
                '<div class="de-panel-subtitle">'
                'Technical details of each dataset column.'
                '</div>',
                unsafe_allow_html=True
            )

            st.dataframe(
                schema_df,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # Traffic label distribution

        st.markdown(
            section_heading(
                "TRAFFIC INTELLIGENCE",
                "Traffic Label Distribution",
                "Understand the distribution of ground-truth traffic labels."
            ),
            unsafe_allow_html=True
        )

        if "Label" in dataset_df.columns:

            label_counts = (
                dataset_df["Label"]
                .astype("string")
                .fillna("Missing")
                .value_counts()
            )

            with st.container(border=True):

                st.markdown(
                    '<div class="de-panel-title">Traffic Class Distribution</div>'
                    '<div class="de-panel-subtitle">'
                    'Number of records belonging to each traffic category.'
                    '</div>',
                    unsafe_allow_html=True
                )

                render_distribution_chart(
                    label_counts.index.astype(str).tolist(),
                    label_counts.values.tolist(),
                    "Number of Records"
                )

        else:

            st.info(
                "This CSV does not contain a Label column. "
                "Ground-truth attack distribution is therefore unavailable."
            )

        st.divider()

        # Feature distribution

        st.markdown(
            section_heading(
                "FEATURE ANALYTICS",
                "Feature Distribution",
                "Select an individual feature to explore its value distribution."
            ),
            unsafe_allow_html=True
        )

        feature_columns = [
            col for col in dataset_df.columns if col != "Label"
        ]

        if feature_columns:

            selected_feature = st.selectbox(
                "Select a feature to explore",
                feature_columns,
                key="dataset_feature_select"
            )

            selected_data = dataset_df[selected_feature]

            st.markdown(
                f'<div class="de-feature-info">'
                f'<b>Selected Feature:</b> {escape(str(selected_feature))}<br>'
                f'<b>Data Type:</b> {escape(str(selected_data.dtype))}<br>'
                f'<b>Unique Values:</b> {selected_data.nunique():,}<br>'
                f'<b>Missing Values:</b> {int(selected_data.isna().sum()):,}'
                f'</div>',
                unsafe_allow_html=True
            )

            if pd.api.types.is_numeric_dtype(selected_data):

                numeric_data = pd.to_numeric(
                    selected_data,
                    errors="coerce"
                ).dropna()

                if numeric_data.empty:

                    st.info(
                        "No numeric values available for this feature."
                    )

                elif numeric_data.nunique() > 15:

                    distribution = (
                        pd.cut(numeric_data, bins=10)
                        .value_counts()
                        .sort_index()
                    )

                    distribution.index = distribution.index.astype(str)

                    with st.container(border=True):

                        st.markdown(
                            '<div class="de-panel-title">Numeric Feature Distribution</div>'
                            '<div class="de-panel-subtitle">'
                            'Values grouped into 10 intervals.'
                            '</div>',
                            unsafe_allow_html=True
                        )

                        render_distribution_chart(
                            distribution.index.tolist(),
                            distribution.values.tolist(),
                            "Number of Records"
                        )

                else:

                    distribution = (
                        numeric_data.value_counts()
                        .sort_index()
                    )

                    distribution.index = distribution.index.astype(str)

                    with st.container(border=True):

                        st.markdown(
                            '<div class="de-panel-title">Value Frequency Distribution</div>'
                            '<div class="de-panel-subtitle">'
                            'Frequency of individual numeric values.'
                            '</div>',
                            unsafe_allow_html=True
                        )

                        render_distribution_chart(
                            distribution.index.tolist(),
                            distribution.values.tolist(),
                            "Number of Records"
                        )

            else:

                distribution = (
                    selected_data.astype("string")
                    .fillna("Missing")
                    .value_counts()
                    .head(15)
                )

                with st.container(border=True):

                    st.markdown(
                        '<div class="de-panel-title">Categorical Feature Distribution</div>'
                        '<div class="de-panel-subtitle">'
                        'Top 15 most frequent values in the selected feature.'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    render_distribution_chart(
                        distribution.index.astype(str).tolist(),
                        distribution.values.tolist(),
                        "Number of Records"
                    )

        else:

            st.info("No features available to display.")
