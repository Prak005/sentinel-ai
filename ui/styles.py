"""Sentinel AI dashboard styling."""

CUSTOM_CSS = r"""@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Rajdhani:wght@500;600;700&display=swap');

/* Main application */
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, rgba(31, 83, 110, 0.15), transparent 40%),
        #08111F;
    color: #E8EEF7;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 12% 0%, rgba(42, 151, 166, 0.13), transparent 34%),
        linear-gradient(180deg, #0A1728 0%, #091321 100%);
    border-right: 1px solid rgba(69, 214, 194, 0.14);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 1.35rem;
    padding-bottom: 1.4rem;
}

/* Sentinel AI brand panel */
.sidebar-brand {
    position: relative;
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 12px 15px;
    margin: 3px 0 27px;
    overflow: hidden;
    border: 1px solid rgba(69, 214, 194, 0.22);
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(20, 48, 68, 0.96), rgba(11, 27, 45, 0.96));
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.20), inset 0 1px 0 rgba(255, 255, 255, 0.035);
}

.sidebar-brand::before {
    content: "";
    position: absolute;
    width: 118px;
    height: 118px;
    top: -68px;
    right: -35px;
    border-radius: 50%;
    background: rgba(69, 214, 194, 0.13);
    filter: blur(22px);
    pointer-events: none;
}

.brand-mark {
    position: relative;
    z-index: 1;
    display: flex;
    flex: 0 0 46px;
    width: 46px;
    height: 46px;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(91, 239, 222, 0.55);
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(69, 214, 194, 0.19), rgba(28, 88, 111, 0.20));
    box-shadow: 0 0 20px rgba(69, 214, 194, 0.13), inset 0 0 13px rgba(69, 214, 194, 0.07);
}

.brand-mark svg {
    width: 29px;
    height: 29px;
    filter: drop-shadow(0 0 5px rgba(69, 214, 194, 0.32));
}

.brand-copy {
    position: relative;
    z-index: 1;
    min-width: 0;
}

.brand-name {
    display: flex;
    align-items: baseline;
    white-space: nowrap;
    color: #F2FAFF;
    font-family: 'Orbitron', 'Arial', sans-serif;
    font-size: 17px;
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: 0.35px;
    text-shadow: 0 0 15px rgba(215, 247, 255, 0.10);
}

.brand-ai {
    margin-left: 4px;
    color: #55E5D4;
    text-shadow: 0 0 12px rgba(69, 214, 194, 0.48);
}

.brand-subtitle {
    margin-top: 6px;
    color: #91B6C5;
    font-family: 'Rajdhani', 'Arial', sans-serif;
    font-size: 11px;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: 1.55px;
    white-space: nowrap;
}

.brand-divider {
    height: 1px;
    margin: -12px 8px 20px;
    background: linear-gradient(90deg, transparent, rgba(69, 214, 194, 0.35), transparent);
}

.side-label {
    color: #6F9AAE;
    font-family: 'Rajdhani', 'Arial', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.2px;
    margin: 17px 0 10px 5px;
}

/* Sidebar navigation */
[data-testid="stSidebar"] [data-testid="stRadio"] > label {
    display: none;
}

[data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
    gap: 5px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    min-height: 39px;
    padding: 7px 10px;
    border: 1px solid transparent;
    border-radius: 10px;
    color: #A8B8CB;
    font-family: 'Rajdhani', 'Arial', sans-serif;
    font-size: 15px;
    font-weight: 600;
    transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    color: #62E8D9;
    background: rgba(69, 214, 194, 0.07);
    border-color: rgba(69, 214, 194, 0.14);
}

[data-testid="stSidebar"] [data-testid="stRadio"] input {
    accent-color: #45D6C2;
}

/* Main heading */
.eyebrow {
    color: #45D6C2;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    margin-bottom: 8px;
}

.main-title {
    color: #F0F5FC;
    font-size: 32px;
    font-weight: 750;
    margin: 0;
    letter-spacing: -0.8px;
}

.subtitle {
    color: #8295AB;
    font-size: 13px;
    margin-top: 8px;
}

.preview-pill {
    background: rgba(245, 190, 97, 0.10);
    color: #F5BE61;
    border: 1px solid rgba(245, 190, 97, 0.25);
    border-radius: 20px;
    padding: 9px 13px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-align: center;
    margin-top: 13px;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(145deg, #14243A, #101D30);
    border: 1px solid rgba(148, 163, 184, 0.13);
    border-radius: 17px;
    padding: 20px;
    min-height: 145px;
    position: relative;
    transition: all 0.2s ease;
}

.metric-card:hover {
    border-color: var(--accent);
    transform: translateY(-3px);
}

.metric-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.metric-label {
    color: #91A4BA;
    font-size: 11px;
    font-weight: 650;
    letter-spacing: 1px;
}

.metric-icon {
    color: var(--accent);
    font-size: 23px;
}

.metric-value {
    color: #F2F6FC;
    font-size: 29px;
    font-weight: 750;
    margin-top: 17px;
    letter-spacing: -1px;
}

.metric-note {
    color: #8295AB;
    font-size: 11px;
    margin-top: 5px;
}

/* Section headings */
.section-heading {
    color: #EAF0F8;
    font-size: 16px;
    font-weight: 700;
    margin: 12px 0 15px 0;
}

.section-caption {
    color: #8295AB;
    font-size: 11px;
    margin-top: -10px;
    margin-bottom: 15px;
}

/* Panel styling */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(16, 29, 48, 0.75);
    border-color: rgba(148, 163, 184, 0.13) !important;
    border-radius: 17px !important;
}

.panel-title {
    color: #EAF0F8;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 3px;
}

.panel-subtitle {
    color: #8295AB;
    font-size: 11px;
    margin-bottom: 15px;
}

/* Alert rows */
.alert-row {
    display: grid;
    grid-template-columns: 85px 1fr 95px;
    align-items: center;
    padding: 13px 5px;
    border-bottom: 1px solid rgba(148, 163, 184, 0.09);
    gap: 12px;
}

.alert-time {
    color: #8295AB;
    font-size: 11px;
}

.alert-event strong {
    color: #E8EEF7;
    font-size: 12px;
}

.alert-event small {
    display: block;
    color: #8295AB;
    font-size: 10px;
    margin-top: 4px;
}

.severity {
    font-size: 9px;
    font-weight: 750;
    text-align: center;
    border-radius: 7px;
    padding: 6px 7px;
    letter-spacing: 0.5px;
}

.critical {
    color: #FF7777;
    background: rgba(255, 90, 90, 0.12);
}

.high {
    color: #F5A36B;
    background: rgba(245, 163, 107, 0.12);
}

.medium {
    color: #F5BE61;
    background: rgba(245, 190, 97, 0.12);
}

.low {
    color: #45D6C2;
    background: rgba(69, 214, 194, 0.12);
}

/* Engine cards */
.engine-card {
    background: #14243A;
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 13px;
    padding: 17px;
}

.engine-name {
    color: #EAF0F8;
    font-size: 14px;
    font-weight: 700;
}

.engine-description {
    color: #8295AB;
    font-size: 11px;
    margin-top: 7px;
}

.engine-status {
    color: #F5BE61;
    font-size: 9px;
    letter-spacing: 1px;
    font-weight: 700;
    margin-top: 14px;
}

/* Sidebar footer - edit its text in app.py whenever you like */
.sidebar-footer {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(18, 43, 62, 0.88), rgba(12, 28, 46, 0.92));
    border: 1px solid rgba(69, 214, 194, 0.17);
    border-radius: 13px;
    padding: 13px 14px 14px;
    margin-top: 34px;
}

.sidebar-footer::before {
    content: "";
    position: absolute;
    top: 0;
    left: 14px;
    width: 42px;
    height: 2px;
    background: #45D6C2;
    box-shadow: 0 0 12px rgba(69, 214, 194, 0.55);
}

.footer-title {
    color: #58DCCF;
    font-family: 'Orbitron', 'Arial', sans-serif;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.25px;
}

.footer-text {
    color: #A8B8CB;
    font-family: 'Rajdhani', 'Arial', sans-serif;
    font-size: 13px;
    font-weight: 600;
    line-height: 1.35;
    margin-top: 7px;
}

/* Upload area */
[data-testid="stFileUploader"] {
    background: #122138;
    border: 1px dashed rgba(69, 214, 194, 0.4);
    border-radius: 14px;
    padding: 15px;
}

.stButton button {
    background: #45D6C2;
    color: #08111F;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

.stButton button:hover {
    background: #69E9D5;
    color: #08111F;
}

/* Footer */
.app-footer {
    color: #53677F;
    text-align: center;
    font-size: 10px;
    margin-top: 35px;
    padding-top: 18px;
    border-top: 1px solid rgba(148, 163, 184, 0.10);
}"""
