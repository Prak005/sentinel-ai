
"""Sentinel AI Overview UI. Detection and inference logic remains unchanged."""
import html
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700&family=Rajdhani:wght@500;600;700&display=swap');

.ov-hero{padding:25px 27px 0;border:1px solid #24505b;border-radius:18px;background:radial-gradient(circle at 90% 0%,#17434a 0,transparent 38%),linear-gradient(120deg,#10283a,#0a1727);margin:5px 0 20px;box-shadow:0 12px 30px #0003}
.ov-main{display:flex;justify-content:space-between;align-items:center;gap:22px;padding-bottom:22px}
.ov-kicker,.ov-label,.ov-index{font:700 10px 'Rajdhani';letter-spacing:1.6px;color:#65c9c2}
.ov-title{font:700 clamp(22px,3vw,34px) 'Orbitron';color:#f1f7fc;margin-top:12px}
.ov-title span{color:#5ce0d1}
.ov-desc{font-size:12px;color:#91a9bb;margin-top:8px}
.ov-mode{min-width:220px;padding:14px;border:1px solid #2a6062;border-radius:12px;background:#071827aa}
.ov-mode b{display:block;font:700 17px 'Rajdhani';letter-spacing:1px;color:#e3fffa;margin-top:4px}
.ov-mode small{color:#7d9aab}
.ov-foot{display:flex;justify-content:space-between;gap:10px;border-top:1px solid #ffffff16;padding:11px 0;color:#9bb2c0;font:700 10px 'Rajdhani';letter-spacing:1px}
.ov-foot b{color:#d7eeef}
.ov-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#5de0c8;box-shadow:0 0 9px #5de0c8;margin-right:8px}
.ov-dot.wait{background:#f4b95f;box-shadow:0 0 9px #f4b95f}

.ov-card{padding:15px 16px;border:1px solid #ffffff20;border-radius:14px;background:linear-gradient(145deg,#142b40,#0c1b2c);min-height:143px;position:relative;overflow:hidden}
.ov-card:before{content:'';position:absolute;left:0;top:0;width:100%;height:2px;background:var(--a)}
.ov-cardtop{display:flex;justify-content:space-between}
.ov-icon{color:var(--a);font-size:19px}
.ov-index{font-size:8px;color:#6c879c}
.ov-metric-label{font:700 11px 'Rajdhani';letter-spacing:1px;color:#a9bdcb;margin-top:13px}
.ov-value{font:700 24px 'Orbitron';color:#f1f6fb;margin-top:4px}
.ov-note{font-size:10px;color:#7891a4;margin-top:4px}
.ov-bottom{border-top:1px solid #ffffff16;margin-top:10px;padding-top:8px;color:#8298a9;font:700 9px 'Rajdhani';letter-spacing:1px}

.ov-section{display:flex;justify-content:space-between;align-items:end;gap:12px;margin:27px 0 12px}
.ov-section small{font:700 9px 'Rajdhani';letter-spacing:1.6px;color:#63b9b5}
.ov-section h3{font:600 17px 'Orbitron';color:#eaf2f8;margin:5px 0}
.ov-section p{font-size:11px;color:#8299aa;margin:0}
.ov-chip{font:700 9px 'Rajdhani';letter-spacing:1px;color:#72c9c2;border:1px solid #3b8b841f;border-radius:20px;padding:6px 10px}

.ov-panel-title{font:700 9px 'Rajdhani';letter-spacing:1.4px;color:#66b9b5}
.ov-panel-title b{display:block;font:600 14px 'Orbitron';letter-spacing:0;color:#e5eef5;margin-top:4px}
.ov-panel-title span{display:block;font:400 10px sans-serif;color:#8299aa;margin-top:4px}
.ov-empty{min-height:210px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;color:#dce8f1}
.ov-empty strong{font:700 16px 'Rajdhani';margin-top:10px}
.ov-empty span{font-size:11px;color:#8197a9;max-width:280px;margin-top:4px}

.ov-risk{padding:12px;border:1px solid color-mix(in srgb,var(--r) 30%,transparent);border-radius:11px;background:#112438;min-height:83px}
.ov-risk label{font:700 9px 'Rajdhani';letter-spacing:1px;color:var(--r)}
.ov-risk b{display:block;font:700 21px 'Orbitron';color:#f2f6fa;margin-top:7px}

.ov-event{display:grid;grid-template-columns:110px minmax(0,1fr) auto;align-items:center;gap:14px;padding:12px;margin-top:8px;border:1px solid #ffffff1c;border-left:3px solid var(--r);border-radius:9px;background:#102337}
.ov-event small{font:700 8px 'Rajdhani';letter-spacing:1px;color:#7792a5}
.ov-event time{display:block;font-size:10px;color:#c5d4df;margin-top:4px;overflow-wrap:anywhere}
.ov-event strong{font:700 15px 'Rajdhani';color:#eff5f9}
.ov-meta{font-size:9px;color:#8ba0b1;margin-top:5px;display:flex;flex-wrap:wrap;gap:5px 12px}
.ov-meta b{color:#62b9b5;margin-right:3px}
.ov-badge{font:700 9px 'Rajdhani';letter-spacing:.6px;color:var(--r);padding:6px 9px;border:1px solid color-mix(in srgb,var(--r) 40%,transparent);border-radius:6px;background:#ffffff08;white-space:nowrap}

@media(max-width:800px){
    .ov-main{align-items:flex-start;flex-direction:column}
    .ov-mode{width:100%}
    .ov-section{align-items:flex-start;flex-direction:column}
    .ov-event{grid-template-columns:1fr;gap:7px}
}
/* ===== SECURITY EVENTS: READABILITY UPGRADE ===== */

/* Risk summary cards */
.ov-risk {
    padding: 16px;
    min-height: 95px;
}

.ov-risk label {
    font-size: 11px;
    letter-spacing: 1.3px;
}

.ov-risk b {
    font-size: 25px;
}

/* Event cards */
.ov-event {
    grid-template-columns: 125px minmax(0, 1fr) auto;
    padding: 16px;
    gap: 16px;
}

/* Timestamp heading */
.ov-event small {
    font-size: 10px;
    letter-spacing: 1.2px;
}

/* Timestamp value */
.ov-event time {
    font-size: 12px;
    line-height: 1.5;
}

/* Attack / anomaly name */
.ov-event strong {
    font-size: 18px;
}

/* Source IP, Destination IP and Score */
.ov-meta {
    font-size: 12px;
    line-height: 1.7;
    gap: 8px 16px;
}

.ov-meta b {
    font-size: 10px;
    letter-spacing: 0.8px;
}

/* Risk badges */
.ov-badge {
    font-size: 11px;
    padding: 8px 11px;
    letter-spacing: 0.8px;
}

/* Event count */
.ov-index {
    font-size: 10px;
}
</style>
"""


def panel(kicker, title, subtitle, number):
    st.markdown(
        f'<div class="ov-panel-title">{kicker}<b>{title}</b><span>{subtitle}</span></div><div style="text-align:right;color:#5d8296;font:700 10px Rajdhani">{number}</div>',
        unsafe_allow_html=True
    )


def render_page():

    st.markdown(CSS, unsafe_allow_html=True)

    df = st.session_state.get("sentinel_analysis_df")
    ready = df is not None and not df.empty and "Final Status" in df.columns

    if ready:
        total = len(df)
        attack_count = int((df["Final Status"] == "Known Attack").sum())
        anomaly_count = int((df["Final Status"] == "Suspicious Anomaly").sum())
        normal_count = int((df["Final Status"] == "Normal").sum())

        status = "NETWORK ANALYSIS COMPLETE"
        dot = ""
        source = "LATEST CSV ANALYSIS"
        note = "Latest analyzed CSV dataset"

    else:
        total = attack_count = anomaly_count = normal_count = "—"
        status = "NO ANALYSIS YET — AWAITING CSV UPLOAD"
        dot = "wait"
        source = "AWAITING DATASET"
        note = "Upload and analyze a CSV to view results"

    # COMMAND CENTER HEADER
    st.markdown(
        f'''<section class="ov-hero">
        <div class="ov-main">
            <div>
                <div class="ov-kicker">◉ SENTINEL AI / SECURITY OPERATIONS CENTER</div>
                <div class="ov-title">Network <span>Command Center</span></div>
                <div class="ov-desc">A unified view of network-flow classification, anomaly signals and threat activity.</div>
            </div>
            <div class="ov-mode">
                <div class="ov-label">ANALYSIS MODE</div>
                <b>NETWORK ANALYSIS</b>
                <small></small>
            </div>
        </div>
        <div class="ov-foot">
            <span><i class="ov-dot {dot}"></i>{status}</span>
            <span>DATA SOURCE <b>{source}</b></span>
        </div>
        </section>''',
        unsafe_allow_html=True
    )

    # METRIC CARDS
    cards = [
        ("TOTAL TRAFFIC FLOWS", "◈", total, "ALL PROCESSED FLOWS", "#58d8cf"),
        ("ATTACKS DETECTED", "⌁", attack_count, "KNOWN ATTACK LABELS", "#ff7180"),
        ("ANOMALIES FLAGGED", "◇", anomaly_count, "SUSPICIOUS BEHAVIOUR", "#f4b95f"),
        ("NORMAL TRAFFIC", "✓", normal_count, "CLASSIFIED AS NORMAL", "#69d9a7"),
    ]

    cols = st.columns(4, gap="medium")

    for i, (col, (label, icon, value, desc, color)) in enumerate(zip(cols, cards), 1):
        shown = f"{value:,}" if isinstance(value, (int, float)) else value

        with col:
            st.markdown(
                f'''<div class="ov-card" style="--a:{color}">
                <div class="ov-cardtop">
                    <span class="ov-icon">{icon}</span>
                    <span class="ov-index">SENTINEL / 0{i}</span>
                </div>
                <div class="ov-metric-label">{label}</div>
                <div class="ov-value">{shown}</div>
                <div class="ov-note">{note}</div>
                <div class="ov-bottom">{desc}</div>
                </div>''',
                unsafe_allow_html=True
            )

    # DETECTION ANALYTICS
    st.markdown(
        '''<div class="ov-section">
        <div>
            <small>01 / TRAFFIC INTELLIGENCE</small>
            <h3>Detection analytics</h3>
            <p>Hybrid classification results from the currently analyzed dataset.</p>
        </div>
        <div class="ov-chip">HYBRID DETECTION ENGINE</div>
        </div>''',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.55, 1], gap="medium")

    if not ready:

        with left:
            with st.container(border=True):
                panel("CLASSIFICATION OUTPUT", "Detection Summary",
                      "Known attacks, suspicious anomalies and normal flows", "01")

                st.markdown(
                    '<div class="ov-empty"><div style="font-size:25px;color:#62d6ca">⌁</div><strong>Awaiting traffic analysis</strong><span>Analyze a compatible CSV in Traffic Analyzer to populate the detection summary.</span></div>',
                    unsafe_allow_html=True
                )

        with right:
            with st.container(border=True):
                panel("FLOW BREAKDOWN", "Traffic Distribution",
                      "Hybrid classification breakdown", "02")

                st.markdown(
                    '<div class="ov-empty"><div style="font-size:25px;color:#62d6ca">◌</div><strong>No dataset loaded</strong><span>The traffic distribution will appear here after analysis.</span></div>',
                    unsafe_allow_html=True
                )

    else:
        known = int((df["Final Status"] == "Known Attack").sum())
        suspicious = int((df["Final Status"] == "Suspicious Anomaly").sum())
        normal = int((df["Final Status"] == "Normal").sum())

        with left:
            with st.container(border=True):
                panel("CLASSIFICATION OUTPUT", "Detection Summary",
                      "Known attacks, suspicious anomalies and normal flows", "01")

                fig = go.Figure(go.Bar(
                    y=["Known Attacks", "Suspicious Anomalies", "Normal"],
                    x=[known, suspicious, normal],
                    orientation="h",
                    marker_color=["#ff7180", "#f4b95f", "#58d8cf"],
                    text=[known, suspicious, normal],
                    texttemplate="%{x:,.0f}",
                    textposition="outside",
                    cliponaxis=False
                ))

                fig.update_layout(
                    height=300,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#a8b8cb", family="Rajdhani"),
                    margin=dict(l=8, r=30, t=12, b=8),
                    showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor="rgba(148,163,184,.1)", showticklabels=False),
                    yaxis=dict(showgrid=False, autorange="reversed")
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        with right:
            with st.container(border=True):
                panel("FLOW BREAKDOWN", "Traffic Distribution",
                      "Hybrid classification breakdown", "02")

                fig = go.Figure(go.Pie(
                    labels=["Normal", "Known Attack", "Suspicious Anomaly"],
                    values=[normal, known, suspicious],
                    hole=.76,
                    sort=False,
                    marker=dict(
                        colors=["#58d8cf", "#ff7180", "#f4b95f"],
                        line=dict(color="#101d30", width=3)
                    ),
                    textinfo="none",
                    hovertemplate="%{label}<br>%{value:,} flows (%{percent})<extra></extra>"
                ))

                fig.update_layout(
                    height=275,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#a8b8cb", family="Rajdhani"),
                    legend=dict(
                        orientation="h", y=-.12, x=.5,
                        xanchor="center", font=dict(size=10)
                    ),
                    margin=dict(l=5, r=5, t=5, b=35),
                    annotations=[dict(
                        text=f"<b>{len(df):,}</b><br><span style='font-size:10px'>TOTAL FLOWS</span>",
                        x=.5, y=.5, showarrow=False,
                        font=dict(size=18, color="#f0f5fc", family="Orbitron")
                    )]
                )

                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # RECENT SECURITY EVENTS
    st.markdown(
        '''<div class="ov-section">
        <div>
            <small>02 / THREAT MONITORING</small>
            <h3>Recent security events</h3>
            <p>Prioritised detections from the latest analyzed traffic file.</p>
        </div>
        <div class="ov-chip">RISK TRIAGE</div>
        </div>''',
        unsafe_allow_html=True
    )

    with st.container(border=True):

        if not ready:
            st.markdown(
                '<div class="ov-empty"><div style="font-size:25px;color:#62d6ca">⌑</div><strong>Security feed is standing by</strong><span>Analyze a traffic CSV to populate detected events and risk priorities.</span></div>',
                unsafe_allow_html=True
            )

        elif "Risk Level" not in df.columns:
            st.warning("Risk classification is unavailable. Please upload the CSV again and click Analyze Traffic.")

        else:
            events = df[
                df["Final Status"].isin(["Known Attack", "Suspicious Anomaly"])
            ].copy()

            if events.empty:
                st.markdown(
                    '<div class="ov-empty"><div style="font-size:25px;color:#69d9a7">✓</div><strong>No security threats detected</strong><span>No known attacks or suspicious anomalies were returned for this analysis.</span></div>',
                    unsafe_allow_html=True
                )

            else:
                # Existing risk labels, attack override, counts and ordering are preserved.
                events["Risk Level"] = (
                    events["Risk Level"].fillna("UNRATED").astype(str).str.upper().str.strip()
                )

                events.loc[
                    events["Final Status"] == "Known Attack",
                    "Risk Level"
                ] = "CONFIRMED ATTACK"

                valid = ["HIGH RISK", "MEDIUM RISK", "LOW RISK"]

                bad = (
                    (events["Final Status"] == "Suspicious Anomaly")
                    & ~events["Risk Level"].isin(valid)
                )

                events.loc[bad, "Risk Level"] = "UNRATED"

                counts = {
                    "HIGH RISK": int((events["Risk Level"] == "HIGH RISK").sum()),
                    "MEDIUM RISK": int((events["Risk Level"] == "MEDIUM RISK").sum()),
                    "LOW RISK": int((events["Risk Level"] == "LOW RISK").sum()),
                    "CONFIRMED ATTACK": int((events["Risk Level"] == "CONFIRMED ATTACK").sum())
                }

                unrated = int((events["Risk Level"] == "UNRATED").sum())

                st.markdown(
                    '<div class="ov-section" style="margin-top:5px"><div><h3 style="font:700 16px Rajdhani;color:#e6eff5;margin:0">Risk overview</h3><p>Calibrated triage labels · not attack probabilities</p></div><div class="ov-chip">PRIORITY COUNTS</div></div>',
                    unsafe_allow_html=True
                )

                risk_cols = st.columns(4, gap="small")

                risk_data = [
                    ("HIGH RISK", "#ff7180"),
                    ("MEDIUM RISK", "#f4b95f"),
                    ("LOW RISK", "#63bdeb"),
                    ("CONFIRMED ATTACK", "#d879e8")
                ]

                for col, (label, color) in zip(risk_cols, risk_data):
                    with col:
                        st.markdown(
                            f'<div class="ov-risk" style="--r:{color}"><label>{label}</label><b>{counts[label]:,}</b></div>',
                            unsafe_allow_html=True
                        )

                if unrated:
                    st.warning(f"{unrated:,} suspicious events have no valid risk classification.")

                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;align-items:center;margin:22px 0 8px"><b style="font:700 16px Rajdhani;color:#e6eff5">Detected events</b><span class="ov-index">{len(events):,} TOTAL</span></div>',
                    unsafe_allow_html=True
                )

                if "Anomaly Score" not in events.columns:
                    events["Anomaly Score"] = float("nan")

                events["Anomaly Score"] = pd.to_numeric(
                    events["Anomaly Score"], errors="coerce"
                )

                events = events.sort_values(
                    "Anomaly Score", ascending=True, na_position="last"
                )

                for _, row in events.head(10).iterrows():

                    status = str(row["Final Status"])
                    rf = str(row.get("RF Prediction", ""))

                    title = (
                        rf if status == "Known Attack" and rf.strip()
                        and rf.lower() != "benign"
                        else ("Known Attack" if status == "Known Attack" else "Suspicious Anomaly")
                    )

                    risk = str(row["Risk Level"])

                    color = {
                        "CONFIRMED ATTACK": "#d879e8",
                        "HIGH RISK": "#ff7180",
                        "MEDIUM RISK": "#f4b95f",
                        "LOW RISK": "#63bdeb"
                    }.get(risk, "#8ba0b1")

                    def val(x):
                        return "Unavailable" if x is None or pd.isna(x) else str(x)

                    score = row.get("Anomaly Score")
                    score_text = f"{score:.5f}" if pd.notna(score) else "Unavailable"

                    safe = [
                        html.escape(x) for x in [
                            title,
                            val(row.get("Timestamp")),
                            val(row.get("Source IP")),
                            val(row.get("Destination IP")),
                            score_text,
                            risk
                        ]
                    ]

                    st.markdown(
                        f'''<div class="ov-event" style="--r:{color}">
                        <div><small>TIMESTAMP</small><time>{safe[1]}</time></div>
                        <div><strong>{safe[0]}</strong>
                            <div class="ov-meta">
                                <span><b>SRC</b>{safe[2]}</span>
                                <span><b>DST</b>{safe[3]}</span>
                                <span><b>SCORE</b>{safe[4]}</span>
                            </div>
                        </div>
                        <div><span class="ov-badge">{safe[5]}</span></div>
                        </div>''',
                        unsafe_allow_html=True
                    )
