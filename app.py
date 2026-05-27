# ═══════════════════════════════════════════════════════════════════════════════
#  고속도로 물류 취약성 & 유류충격 분석 대시보드
#  Expressway Logistics Vulnerability & Fuel Shock Impact Analysis System
# ═══════════════════════════════════════════════════════════════════════════════
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings, time, json, os
warnings.filterwarnings("ignore")

# ── 페이지 설정 ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="고속도로 물류 취약성 분석 시스템",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS / 테마 ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Mono:wght@400;500&display=swap');

/* ── TOKENS ── */
:root {
  --bg:         #f8f9fc;
  --surface:    #ffffff;
  --raised:     #f2f4f8;
  --border:     rgba(0,0,0,.08);
  --border-hi:  rgba(0,0,0,.16);
  --text-1:     #0f1117;
  --text-2:     #5a6178;
  --text-3:     #9aa0b4;
  --accent:     #2b50d8;
  --accent-lo:  rgba(43,80,216,.08);
  --red:        #d93025;
  --red-lo:     rgba(217,48,37,.08);
  --amber:      #c47d00;
  --amber-lo:   rgba(196,125,0,.08);
  --green:      #1a7f4b;
  --green-lo:   rgba(26,127,75,.08);
  --mono:       'DM Mono', monospace;
  --shadow-sm:  0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
  --shadow-md:  0 4px 12px rgba(0,0,0,.07), 0 2px 4px rgba(0,0,0,.04);
}

html, body, [class*="css"], [class*="st-"] {
  font-family: 'DM Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
}
.stApp { background: var(--bg) !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  box-shadow: var(--shadow-sm) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
  font-size: 11px !important; font-weight: 600 !important;
  letter-spacing: .06em !important; color: var(--text-3) !important;
  text-transform: uppercase !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background: var(--raised) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important; color: var(--text-1) !important;
}

/* ── SIDEBAR HELPERS ── */
.sb-logo { display:flex; align-items:center; gap:12px; padding:20px 0 18px; border-bottom:1px solid var(--border); margin-bottom:2px; }
.sb-logo-icon { width:38px; height:38px; border-radius:10px; background:var(--accent-lo); border:1px solid rgba(43,80,216,.2); display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }
.sb-logo-title { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:var(--text-1); line-height:1.2; }
.sb-logo-sub   { font-size:10px; color:var(--text-3); letter-spacing:.04em; margin-top:2px; }
.sb-section    { font-size:9px; font-weight:700; letter-spacing:.12em; color:var(--text-3); text-transform:uppercase; padding:18px 0 8px; border-bottom:1px solid var(--border); margin-bottom:12px; }
.sb-stat       { background:var(--raised); border:1px solid var(--border); border-radius:10px; padding:10px 14px; text-align:center; flex:1; }
.sb-stat-val   { font-family:var(--mono); font-size:20px; font-weight:500; color:var(--text-1); line-height:1; margin-bottom:4px; }
.sb-stat-lbl   { font-size:9px; color:var(--text-3); letter-spacing:.06em; text-transform:uppercase; }
.sb-stat.danger  { border-color:rgba(217,48,37,.2); } .sb-stat.danger  .sb-stat-val { color:var(--red); }
.sb-stat.success .sb-stat-val { color:var(--green); }

/* ── TOP BAR ── */
.topbar { display:flex; align-items:center; justify-content:space-between; padding:16px 28px; margin:-1rem -1rem 24px; background:var(--surface); border-bottom:1px solid var(--border); box-shadow:var(--shadow-sm); }
.topbar-left { display:flex; align-items:center; gap:16px; }
.topbar-eyebrow { font-size:9px; font-weight:700; letter-spacing:.14em; color:var(--accent); text-transform:uppercase; margin-bottom:4px; }
.topbar-title { font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:var(--text-1); line-height:1; }
.topbar-sub   { font-size:12px; color:var(--text-2); margin-top:3px; }
.topbar-pill  { display:flex; align-items:center; gap:6px; background:var(--raised); border:1px solid var(--border); border-radius:100px; padding:6px 14px; box-shadow:var(--shadow-sm); }
.topbar-pill-dot { width:6px; height:6px; border-radius:50%; background:var(--green); flex-shrink:0; box-shadow:0 0 0 3px var(--green-lo); animation:live-pulse 2.4s ease-in-out infinite; }
@keyframes live-pulse { 0%,100%{box-shadow:0 0 0 3px var(--green-lo);} 50%{box-shadow:0 0 0 6px transparent;} }
.topbar-pill-label { font-size:11px; color:var(--green); font-weight:600; }
.topbar-pill-time  { font-family:var(--mono); font-size:11px; color:var(--text-3); margin-left:4px; }

/* ── ALERTS ── */
.alert { display:flex; align-items:flex-start; gap:12px; border-radius:12px; padding:13px 16px; margin-bottom:16px; }
.alert-icon { font-size:15px; flex-shrink:0; margin-top:1px; }
.alert-title { font-size:12px; font-weight:600; margin-bottom:2px; }
.alert-msg   { font-size:12px; line-height:1.5; }
.alert.critical { background:var(--red-lo); border:1px solid rgba(217,48,37,.2); }
.alert.critical .alert-title, .alert.critical .alert-msg { color:var(--red); }
.alert.warning  { background:var(--amber-lo); border:1px solid rgba(196,125,0,.2); }
.alert.warning  .alert-title, .alert.warning  .alert-msg { color:var(--amber); }

/* ── KPI CARDS ── */
.kpi { position:relative; overflow:hidden; background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:20px 22px 18px; box-shadow:var(--shadow-sm); transition:box-shadow .2s, transform .15s; }
.kpi:hover { box-shadow:var(--shadow-md); transform:translateY(-1px); }
.kpi::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:var(--kpi-accent,var(--accent)); opacity:0; transition:opacity .2s; }
.kpi:hover::before { opacity:1; }
.kpi-eyebrow { font-size:9px; font-weight:700; letter-spacing:.12em; color:var(--text-3); text-transform:uppercase; margin-bottom:8px; }
.kpi-value { font-family:var(--mono); font-size:26px; font-weight:500; color:var(--text-1); line-height:1; margin-bottom:8px; }
.kpi-delta { display:inline-flex; align-items:center; gap:4px; font-size:11px; font-weight:600; padding:3px 8px; border-radius:100px; }
.kpi-delta.up      { background:var(--red-lo);   color:var(--red); }
.kpi-delta.down    { background:var(--green-lo); color:var(--green); }
.kpi-delta.neutral { background:var(--accent-lo);color:var(--accent); }
.kpi.accent-red   { --kpi-accent:var(--red); }
.kpi.accent-amber { --kpi-accent:var(--amber); }
.kpi.accent-green { --kpi-accent:var(--green); }
.kpi.accent-blue  { --kpi-accent:var(--accent); }

/* ── SECTION HEADS ── */
.sec-head { display:flex; align-items:baseline; gap:10px; margin:0 0 14px; padding-bottom:10px; border-bottom:1px solid var(--border); }
.sec-head-title { font-family:'Syne',sans-serif; font-size:13px; font-weight:600; color:var(--text-1); }
.sec-head-sub   { font-size:11px; color:var(--text-3); }

/* ── MAP CHROME ── */
.map-header { display:flex; align-items:center; justify-content:space-between; background:var(--surface); border:1px solid var(--border); border-radius:12px 12px 0 0; border-bottom:none; padding:12px 18px; box-shadow:var(--shadow-sm); }
.map-title  { font-family:'Syne',sans-serif; font-size:13px; font-weight:600; color:var(--text-1); }
.map-desc   { font-size:11px; color:var(--text-3); margin-top:2px; }
.map-badge  { font-family:var(--mono); font-size:11px; color:var(--text-2); background:var(--raised); border:1px solid var(--border); border-radius:100px; padding:4px 12px; }
.map-wrap   { border:1px solid var(--border); border-radius:0 0 12px 12px; overflow:hidden; box-shadow:var(--shadow-sm); }

/* ── LEGEND ── */
.legend-row  { display:flex; gap:8px; flex-wrap:wrap; padding:10px 0 14px; }
.legend-chip { display:flex; align-items:center; gap:7px; background:var(--surface); border:1px solid var(--border); border-radius:100px; padding:5px 12px 5px 8px; box-shadow:var(--shadow-sm); }
.legend-dot  { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
.legend-name { font-size:11px; font-weight:500; color:var(--text-1); }
.legend-count{ font-family:var(--mono); font-size:10px; color:var(--text-3); margin-left:2px; }

/* ── CARD ── */
.card { background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:18px 20px; box-shadow:var(--shadow-sm); }
.card + .card { margin-top:12px; }

/* ── FORECAST ROW ── */
.fc-row { display:grid; grid-template-columns:48px 1fr 72px 40px; align-items:center; gap:10px; background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:9px 14px; margin-bottom:5px; box-shadow:var(--shadow-sm); transition:border-color .15s; }
.fc-row:hover { border-color:var(--border-hi); }
.fc-date  { font-family:var(--mono); font-size:11px; color:var(--text-2); }
.fc-price { font-family:var(--mono); font-size:14px; font-weight:500; color:var(--text-1); }
.fc-si    { font-family:var(--mono); font-size:11px; text-align:right; }
.fc-bar   { height:4px; background:var(--raised); border-radius:2px; overflow:hidden; }
.fc-bar-fill { height:100%; border-radius:2px; }

/* ── GRADE ROWS ── */
.grade-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.grade-label-wrap { display:flex; align-items:center; gap:8px; min-width:110px; }
.grade-dot  { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
.grade-label { font-size:12px; font-weight:500; color:var(--text-1); }
.grade-bar-track { flex:1; height:4px; background:var(--raised); border-radius:2px; margin:0 12px; overflow:hidden; border:1px solid var(--border); }
.grade-bar-fill  { height:100%; border-radius:2px; }
.grade-count { font-family:var(--mono); font-size:11px; color:var(--text-3); min-width:40px; text-align:right; }

/* ── STAT ROW ── */
.stat-row { display:flex; align-items:center; justify-content:space-between; padding:8px 0; border-bottom:1px solid var(--border); font-size:12px; }
.stat-row:last-child { border-bottom:none; }
.stat-key { color:var(--text-2); }
.stat-val { font-family:var(--mono); font-weight:500; color:var(--text-1); }

/* ── INDICATOR CARD ── */
.ind-card  { display:flex; align-items:center; gap:12px; background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:10px 14px; margin-bottom:6px; box-shadow:var(--shadow-sm); }
.ind-ring  { width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-family:var(--mono); font-size:10px; font-weight:600; flex-shrink:0; }
.ind-title { font-size:12px; font-weight:500; color:var(--text-1); margin-bottom:2px; }
.ind-desc  { font-size:10px; color:var(--text-3); }
.ind-code  { font-family:var(--mono); font-size:9px; color:var(--text-3); margin-top:1px; }

/* ── BADGES ── */
.badge { display:inline-flex; align-items:center; gap:5px; padding:3px 10px; border-radius:100px; font-size:10px; font-weight:700; letter-spacing:.04em; }
.badge-vh  { background:var(--red-lo);   color:var(--red);   border:1px solid rgba(217,48,37,.2); }
.badge-hi  { background:var(--amber-lo); color:var(--amber); border:1px solid rgba(196,125,0,.2); }
.badge-mod { background:var(--green-lo); color:var(--green); border:1px solid rgba(26,127,75,.2); }
.badge-low { background:var(--accent-lo);color:var(--accent);border:1px solid rgba(43,80,216,.2); }

/* ── IMPACT CARD ── */
.impact-card { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:14px 16px; margin-bottom:8px; box-shadow:var(--shadow-sm); }
.impact-card-top { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.impact-card-num { font-family:var(--mono); font-size:24px; font-weight:500; }
.impact-card-meta{ display:flex; justify-content:space-between; font-size:11px; color:var(--text-3); margin-bottom:6px; }
.impact-card-bar { height:3px; background:var(--raised); border-radius:2px; overflow:hidden; }
.impact-card-bar-fill { height:100%; border-radius:2px; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { background:var(--surface) !important; gap:0 !important; border-bottom:2px solid var(--border) !important; padding:0 !important; box-shadow:var(--shadow-sm); }
.stTabs [data-baseweb="tab"] { font-family:'DM Sans',sans-serif !important; font-size:12px !important; font-weight:500 !important; color:var(--text-3) !important; background:transparent !important; border:none !important; border-radius:0 !important; padding:11px 20px !important; letter-spacing:.02em !important; }
.stTabs [data-baseweb="tab"]:hover { color:var(--text-1) !important; background:var(--raised) !important; }
.stTabs [aria-selected="true"] { color:var(--accent) !important; font-weight:600 !important; border-bottom:2px solid var(--accent) !important; }
.stTabs [data-baseweb="tab-panel"] { padding:24px 0 0 !important; }

/* ── AI CHAT ── */
.agent-header { display:flex; align-items:center; gap:14px; background:var(--surface); border:1px solid var(--border); border-radius:14px; padding:16px 20px; margin-bottom:16px; box-shadow:var(--shadow-sm); }
.agent-avatar { width:42px; height:42px; border-radius:12px; background:var(--accent-lo); border:1px solid rgba(43,80,216,.2); display:flex; align-items:center; justify-content:center; font-size:20px; flex-shrink:0; }
.agent-name { font-family:'Syne',sans-serif; font-size:14px; font-weight:700; color:var(--text-1); }
.agent-sub  { font-size:11px; color:var(--text-3); margin-top:2px; }
.agent-tools-row { display:flex; gap:5px; flex-wrap:wrap; margin-top:8px; }
.agent-tool-chip { font-family:var(--mono); font-size:9px; color:var(--accent); background:var(--accent-lo); border:1px solid rgba(43,80,216,.15); border-radius:4px; padding:2px 7px; }

.chat-wrap { background:var(--raised); border:1px solid var(--border); border-radius:14px; padding:16px; max-height:440px; overflow-y:auto; margin-bottom:12px; }
.msg-user  { background:var(--accent); border-radius:12px 12px 3px 12px; padding:10px 14px; margin:8px 0; margin-left:16%; font-size:13px; color:#fff; }
.msg-agent { background:var(--surface); border:1px solid var(--border); border-radius:12px 12px 12px 3px; padding:12px 16px; margin:8px 0; margin-right:12%; font-size:13px; color:var(--text-1); line-height:1.65; box-shadow:var(--shadow-sm); }
.msg-agent-name { font-size:9px; font-weight:700; letter-spacing:.1em; color:var(--accent); text-transform:uppercase; margin-bottom:6px; }
.think-step { background:var(--raised); border:1px solid var(--border); border-left:2px solid var(--accent); border-radius:0 6px 6px 0; padding:5px 10px; margin:4px 0; font-family:var(--mono); font-size:10px; color:var(--text-3); }
.think-label { color:var(--accent); font-weight:500; }
.quick-btn-label { font-size:9px; font-weight:700; letter-spacing:.08em; color:var(--text-3); text-transform:uppercase; margin-bottom:6px; }

.tool-card { background:var(--surface); border:1px solid var(--border); border-radius:10px; padding:11px 14px; margin-bottom:6px; box-shadow:var(--shadow-sm); transition:border-color .15s; }
.tool-card:hover { border-color:var(--border-hi); }
.tool-card-top { display:flex; align-items:center; gap:8px; margin-bottom:3px; }
.tool-card-icon { font-size:14px; }
.tool-card-name { font-family:var(--mono); font-size:11px; color:var(--accent); font-weight:500; }
.tool-card-desc { font-size:11px; color:var(--text-3); padding-left:22px; }
.ctx-row  { display:flex; justify-content:space-between; align-items:center; padding:7px 0; border-bottom:1px solid var(--border); font-size:11px; }
.ctx-row:last-child { border-bottom:none; }
.ctx-key  { color:var(--text-2); }
.ctx-val  { font-family:var(--mono); font-weight:500; color:var(--text-1); }

/* ── FORMULA BANNER ── */
.formula-banner { background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--accent); border-radius:0 12px 12px 0; padding:14px 20px; margin-bottom:20px; box-shadow:var(--shadow-sm); }
.formula-label { font-size:9px; font-weight:700; letter-spacing:.12em; color:var(--text-3); text-transform:uppercase; margin-bottom:6px; }
.formula-expr  { font-family:var(--mono); font-size:13px; color:var(--accent); }
.formula-note  { font-size:11px; color:var(--text-2); margin-top:5px; }

/* ── DATAFRAME ── */
.stDataFrame { border-radius:12px !important; overflow:hidden !important; }
[data-testid="stDataFrameResizable"] { background:var(--surface) !important; border:1px solid var(--border) !important; border-radius:12px !important; box-shadow:var(--shadow-sm) !important; }

/* ── BUTTONS ── */
.stButton > button { background:var(--surface) !important; border:1px solid var(--border) !important; color:var(--text-2) !important; border-radius:8px !important; font-size:12px !important; font-weight:500 !important; font-family:'DM Sans',sans-serif !important; transition:all .15s !important; padding:7px 14px !important; box-shadow:var(--shadow-sm) !important; }
.stButton > button:hover { border-color:var(--accent) !important; color:var(--accent) !important; background:var(--accent-lo) !important; }
.stButton > button[kind="primary"] { background:var(--accent) !important; border-color:transparent !important; color:#fff !important; box-shadow:0 2px 8px rgba(43,80,216,.25) !important; }
.stButton > button[kind="primary"]:hover { background:#1e40c0 !important; }

/* ── TEXT INPUT ── */
.stTextInput > div > div > input { background:var(--surface) !important; color:var(--text-1) !important; border:1px solid var(--border) !important; border-radius:8px !important; font-size:13px !important; font-family:'DM Sans',sans-serif !important; box-shadow:var(--shadow-sm) !important; }
.stTextInput > div > div > input:focus { border-color:var(--accent) !important; box-shadow:0 0 0 3px var(--accent-lo) !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--raised); }
::-webkit-scrollbar-thumb { background:var(--border-hi); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--text-3); }

/* ── SLIDERS ── */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { background:var(--accent) !important; border-color:var(--accent) !important; }
hr { border-color:var(--border) !important; margin:20px 0 !important; }

/* ── MINI STAT CARDS ── */
.mini-stat { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:14px 16px; text-align:center; box-shadow:var(--shadow-sm); }
.mini-stat-val { font-family:var(--mono); font-size:22px; font-weight:500; margin-bottom:4px; }
.mini-stat-lbl { font-size:9px; color:var(--text-3); text-transform:uppercase; letter-spacing:.08em; }

/* ── WAR STAT ── */
.war-stat { background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:12px 16px; box-shadow:var(--shadow-sm); }
.war-stat-lbl { font-size:9px; color:var(--text-3); text-transform:uppercase; letter-spacing:.08em; margin-bottom:5px; }
.war-stat-val { font-family:var(--mono); font-size:17px; font-weight:500; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  데이터 생성 / 로드 레이어
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=3600)
def load_energy_data():
    """국제 에너지 지표 시계열 생성 (실제 CSV 기반 재현)"""
    np.random.seed(42)
    dates = pd.date_range("2025-02-01", "2026-05-01", freq="D")
    n = len(dates)
    _war_ts  = pd.Timestamp("2026-02-28")
    war_idx  = np.array([1.0 if d >= _war_ts else 0.0 for d in dates])
    war_days = np.array([float((d - _war_ts).days) if d >= _war_ts else 0.0 for d in dates])
    wti_base = 62 + np.cumsum(np.random.randn(n) * 0.8)
    wti_war_shock = war_idx * np.clip(war_days * 0.3, 0, 45)
    wti = np.clip(wti_base + wti_war_shock + np.random.randn(n) * 1.2, 55, 113)

    brent = wti + np.random.randn(n) * 1.5 + 4.5

    # USD/KRW: 1350~1520
    usdkrw_base = 1390 + np.cumsum(np.random.randn(n) * 2)
    usdkrw_war  = war_idx * np.clip(war_days * 0.5, 0, 90)
    usdkrw = np.clip(usdkrw_base + usdkrw_war, 1352, 1520)

    # VIX: 전쟁 후 급등
    vix_base = 16 + np.cumsum(np.random.randn(n) * 0.5)
    vix_war  = war_idx * np.exp(-war_days / 30) * 36
    vix = np.clip(vix_base + vix_war, 13, 52)

    # 경유가 (국내): WTI + 환율 연동
    diesel_base = 1580 + (wti - 62) * 6.5 + (usdkrw - 1390) * 0.8
    diesel = np.clip(diesel_base + np.random.randn(n) * 5, 1490, 2005)

    df = pd.DataFrame({
        "date": dates, "wti": np.round(wti, 2), "brent": np.round(brent, 2),
        "usd_krw": np.round(usdkrw, 1), "vix": np.round(vix, 2),
        "diesel_price": np.round(diesel, 1),
        "war_period": np.where(dates < pd.Timestamp("2026-02-28"), "전쟁 이전", "전쟁 이후"),
    })
    return df


@st.cache_data(ttl=3600)
def build_forecast(energy_df):
    """30일 경유가 앙상블 예측 (Prophet 40% + LSTM 60% 모의)"""
    last_price = energy_df["diesel_price"].iloc[-1]
    last_date  = energy_df["date"].iloc[-1]
    future_dates = pd.date_range(last_date + timedelta(1), periods=30, freq="D")
    np.random.seed(7)

    trend = np.linspace(0, 35, 30)
    prophet_pred = last_price + trend + np.random.randn(30) * 8
    lstm_pred    = last_price + trend * 1.15 + np.random.randn(30) * 6
    ensemble     = 0.4 * prophet_pred + 0.6 * lstm_pred

    change_rate = (ensemble / last_price - 1) * 100
    r_min, r_max = change_rate.min(), change_rate.max()
    shock_index  = (change_rate - r_min) / (r_max - r_min + 1e-8)

    def grade(x):
        if x < 0.3:   return "LOW"
        elif x < 0.6: return "MEDIUM"
        elif x < 0.8: return "HIGH"
        else:          return "CRITICAL"

    return pd.DataFrame({
        "date": future_dates,
        "prophet": np.round(prophet_pred, 1),
        "lstm": np.round(lstm_pred, 1),
        "ensemble": np.round(ensemble, 1),
        "change_rate": np.round(change_rate, 2),
        "shock_index": np.round(shock_index, 4),
        "risk_level": [grade(x) for x in shock_index],
        "lower": np.round(ensemble - 45, 1),
        "upper": np.round(ensemble + 55, 1),
    })


@st.cache_data(ttl=3600)
def build_unit_data():
    """실제 TCS unitCode 기반 476개 영업소 취약성 지수 산출"""
    np.random.seed(42)

    # ── 실제 unitCode → 영업소명·노선·좌표 매핑 ──
    REAL_UNITS = {
        2:('서울TG','경부고속도로',37.4562,127.0563), 3:('한남','경부고속도로',37.5227,127.0086),
        11:('신탄진','경부고속도로',36.4178,127.3980), 12:('북대전','경부고속도로',36.3917,127.3695),
        13:('남대전','경부고속도로',36.3021,127.3921), 25:('회덕JC','경부고속도로',36.4419,127.4102),
        29:('옥천','경부고속도로',36.2943,127.5726), 53:('추풍령','경부고속도로',36.2179,127.8153),
        56:('황간','경부고속도로',36.1453,127.9165), 57:('영동','경부고속도로',36.1695,127.7803),
        58:('금강','경부고속도로',36.0857,127.6542), 59:('김천','경부고속도로',36.1389,128.1137),
        61:('구미','경부고속도로',36.1194,128.3446), 62:('칠곡','경부고속도로',35.9928,128.4016),
        63:('동대구','경부고속도로',35.8714,128.6241), 64:('경산','경부고속도로',35.8253,128.7316),
        65:('언양','경부고속도로',35.5533,129.1043), 66:('서울산','경부고속도로',35.5867,129.2089),
        67:('부산','경부고속도로',35.2559,129.0533), 68:('기장','경부고속도로',35.2447,129.2235),
        69:('서부산','경부고속도로',35.1561,128.9769), 73:('양재','경부고속도로',37.4681,127.0278),
        74:('판교','경부고속도로',37.3903,127.1095), 91:('북수원','경부고속도로',37.2887,127.0142),
        92:('수원','경부고속도로',37.2612,127.0389),
        101:('서울','경부고속도로',37.5045,127.0289), 102:('강남','경부고속도로',37.4876,127.0591),
        103:('금토','경부고속도로',37.4113,127.1022), 104:('오산','경부고속도로',37.1518,127.0764),
        105:('천안','경부고속도로',36.8132,127.1571), 106:('공주','경부고속도로',36.4456,127.1186),
        107:('논산','경부고속도로',36.1924,127.0991), 108:('익산','호남고속도로',35.9483,126.9774),
        109:('삼례','호남고속도로',35.9091,127.0337), 110:('전주','호남고속도로',35.8241,127.1103),
        111:('순천','호남고속도로',34.9503,127.4875), 112:('광양','남해고속도로',34.9091,127.6919),
        113:('부산신항','남해고속도로',35.0715,128.7832),
        190:('부산신항IC','남해고속도로',35.0821,128.7654),
        252:('양산','남해고속도로',35.3356,129.0275), 253:('동부산','남해고속도로',35.2168,129.1384),
        254:('장유','남해고속도로',35.2011,128.8712), 285:('칠원','남해고속도로',35.2654,128.5428),
        287:('함안','남해고속도로',35.2732,128.4068), 288:('마산','남해고속도로',35.2145,128.5791),
        289:('진주','남해고속도로',35.1803,128.1072), 290:('사천','남해고속도로',35.0621,128.0814),
        291:('광양JC','남해고속도로',34.9503,127.7065),
        500:('서서울','서해안고속도로',37.5068,126.8124), 501:('안산','서해안고속도로',37.3214,126.8012),
        502:('비봉','서해안고속도로',37.2159,126.7836), 503:('발안','서해안고속도로',37.1289,126.7521),
        504:('서평택','서해안고속도로',36.9893,126.8214), 505:('안중','서해안고속도로',36.9012,126.8573),
        506:('서평택JC','서해안고속도로',36.9342,126.9012), 507:('평택시흥','서해안고속도로',37.0651,126.8692),
        602:('원주','영동고속도로',37.3425,127.9203), 603:('여주','영동고속도로',37.2918,127.6371),
        604:('이천','영동고속도로',37.2701,127.4437), 605:('호법JC','영동고속도로',37.2234,127.3876),
        606:('강릉','영동고속도로',37.7519,128.8762), 607:('강릉JC','영동고속도로',37.6843,128.7234),
        608:('속초','동해고속도로',38.2076,128.5912), 612:('횡성','영동고속도로',37.4913,127.9841),
        613:('둔내','영동고속도로',37.5687,128.1456),
        622:('동홍천','영동고속도로',37.6891,128.0123), 641:('동광주','호남고속도로',35.1401,126.9213),
        642:('담양','호남고속도로',35.3212,126.9876), 643:('순창','호남고속도로',35.3745,127.1382),
        644:('남원','호남고속도로',35.4167,127.3912), 645:('함양','호남고속도로',35.5123,127.7234),
        646:('거창','중앙고속도로',35.6871,127.9123), 647:('합천','중앙고속도로',35.5673,128.1654),
        648:('고령','중앙고속도로',35.7234,128.2654),
        651:('김해','남해고속도로',35.2345,128.8905), 652:('장유IC','남해고속도로',35.2011,128.8712),
        653:('진해','남해고속도로',35.1534,128.6921), 654:('마산IC','남해고속도로',35.2145,128.5791),
        655:('의창','남해고속도로',35.2456,128.5123), 656:('함안IC','남해고속도로',35.2732,128.4068),
        657:('군북','남해고속도로',35.3012,128.2891), 658:('의령','남해고속도로',35.3214,128.1567),
        671:('고성','남해고속도로',34.9734,128.3217), 672:('통영','남해고속도로',34.8454,128.4211),
        673:('거제','남해고속도로',34.8801,128.6234), 675:('옥포','남해고속도로',35.0123,128.7456),
        676:('장승포','남해고속도로',34.8654,128.8123), 677:('성산','남해고속도로',34.8912,128.6789),
        681:('창원JC','남해고속도로',35.2289,128.6821), 682:('창원','남해고속도로',35.2145,128.6234),
        683:('마산합포','남해고속도로',35.1892,128.5432), 684:('함안JC','남해고속도로',35.2732,128.4068),
        685:('칠원JC','남해고속도로',35.2654,128.5428),
        700:('광주','호남고속도로',35.1596,126.8526), 701:('동광주IC','호남고속도로',35.1401,126.9213),
        702:('광산','호남고속도로',35.1890,126.7834), 703:('나주','호남고속도로',35.0312,126.7105),
        704:('함평','호남고속도로',35.0643,126.5168), 705:('무안','호남고속도로',34.9891,126.4834),
        706:('목포','호남고속도로',34.8123,126.4235),
    }

    ROUTE_BY_RANGE = {
        (1,99):'경부고속도로', (100,199):'경부고속도로', (200,299):'남해고속도로',
        (300,399):'중앙고속도로', (500,599):'서해안고속도로', (600,699):'영동고속도로',
        (700,799):'호남고속도로', (800,999):'기타고속도로',
    }
    COORD_BY_ROUTE = {
        '경부고속도로':  {'lat':(35.1,37.5),'lon':(126.9,127.6)},
        '남해고속도로':  {'lat':(34.8,35.4),'lon':(127.0,129.2)},
        '서해안고속도로':{'lat':(34.7,37.6),'lon':(126.2,126.9)},
        '영동고속도로':  {'lat':(37.0,38.2),'lon':(127.0,129.0)},
        '호남고속도로':  {'lat':(34.8,36.3),'lon':(126.4,127.2)},
        '중앙고속도로':  {'lat':(35.0,37.8),'lon':(128.3,128.9)},
        '기타고속도로':  {'lat':(35.0,38.0),'lon':(126.5,129.0)},
    }

    def get_route(code):
        for (lo,hi), r in ROUTE_BY_RANGE.items():
            if lo <= code <= hi: return r
        return '기타고속도로'

    # ── 실제 TCS 교통량 집계 ──
    try:
        tcs = pd.read_csv('use_data/use_data/tcs_daily_20250101_20260517.csv')
    except Exception:
        tcs = None

    all_codes = [2,3,11,12,13,25,29,53,56,57,58,59,61,62,63,64,65,66,67,68,69,73,74,91,92,
        101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,
        122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,142,143,
        144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,
        165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,
        186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,
        207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,
        228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,
        249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,
        270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,
        291,292,293,294,295,296,297,298,299,324,325,326,327,331,332,333,
        500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,
        521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,
        542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,
        563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,
        584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,601,602,603,604,605,
        606,607,608,612,613,618,621,622,623,624,625,626,627,628,629,641,642,643,644,645,646,
        647,648,651,652,653,654,655,656,657,658,671,672,673,675,676,677,681,682,683,684,685,
        700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,
        721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,
        742,743,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,762,763,764,765,
        766,767,768,770,771,772,773,774,775,776,777,778,779,780,781,782,783,785,786,787,788,
        789,790,791,795,797,798,799,876,981,982,983,984,985,986,987]

    # TCS 집계
    if tcs is not None:
        unit_agg = tcs.groupby('unitCode').agg(
            mean_freight_share=('freight_345_share','mean'),
            mean_freight_traffic=('freight_345_traffic','mean'),
            std_freight=('freight_345_traffic','std'),
            mean_total=('total_traffic','mean'),
        ).reset_index()
        unit_agg['traffic_volatility'] = (
            unit_agg['std_freight'] / (unit_agg['mean_freight_traffic'] + 1)
        ).fillna(0)
        # 입출구 불균형
        if 'inoutType' in tcs.columns:
            io = tcs.groupby(['unitCode','inoutType'])['freight_345_traffic'].mean().unstack(fill_value=0)
            io.columns = [f'io_{c}' for c in io.columns]
            io = io.reset_index()
            if 'io_0' in io.columns and 'io_1' in io.columns:
                io['abs_imbalance_ratio'] = (
                    np.abs(io['io_0'] - io['io_1']) / (io['io_0'] + io['io_1'] + 1)
                )
            else:
                io['abs_imbalance_ratio'] = 0.0
            unit_agg = unit_agg.merge(io[['unitCode','abs_imbalance_ratio']], on='unitCode', how='left')
            unit_agg['abs_imbalance_ratio'] = unit_agg['abs_imbalance_ratio'].fillna(0)
        else:
            unit_agg['abs_imbalance_ratio'] = np.random.uniform(0, 0.4, len(unit_agg))
        tcs_map = unit_agg.set_index('unitCode').to_dict('index')
    else:
        tcs_map = {}

    # ── 전체 영업소 레코드 생성 ──
    rows = []
    for code in all_codes:
        if code in REAL_UNITS:
            name, route, lat, lon = REAL_UNITS[code]
        else:
            route = get_route(code)
            cr = COORD_BY_ROUTE.get(route, COORD_BY_ROUTE['기타고속도로'])
            lat = round(np.random.uniform(*cr['lat']), 4)
            lon = round(np.random.uniform(*cr['lon']), 4)
            name = f'{route[:2]}{code:03d}'

        if code in tcs_map:
            d = tcs_map[code]
            fs  = float(d['mean_freight_share'])
            ft  = float(d['mean_freight_traffic'])
            vol = float(d['traffic_volatility'])
            imb = float(d['abs_imbalance_ratio'])
        else:
            base = 0.12 if '경부' in route or '남해' in route else 0.08
            fs  = float(np.clip(base + np.random.randn()*0.04, 0.02, 0.42))
            ft  = float(max(10, np.random.lognormal(5.5, 1.0)))
            vol = float(np.clip(np.random.exponential(0.4), 0.05, 5.0))
            imb = float(np.clip(np.abs(np.random.randn()*0.25), 0.0, 0.9))

        rows.append({'unitCode':code,'unitName':name,'routeName':route,
                     'lat':lat,'lon':lon,
                     'mean_freight_share':round(fs,4),
                     'mean_freight_traffic':round(ft,1),
                     'traffic_volatility':round(vol,3),
                     'abs_imbalance_ratio':round(imb,3)})

    df = pd.DataFrame(rows)

    # MinMax 정규화 → Vulnerability Score
    for col in ['mean_freight_share','mean_freight_traffic','traffic_volatility','abs_imbalance_ratio']:
        mn, mx = df[col].min(), df[col].max()
        df[col+'_s'] = (df[col] - mn) / (mx - mn + 1e-9)

    df['vulnerability_score'] = (
        0.30*df['mean_freight_share_s'] + 0.30*df['mean_freight_traffic_s'] +
        0.20*df['traffic_volatility_s'] + 0.20*df['abs_imbalance_ratio_s']
    ).round(4)
    df = df.drop(columns=[c for c in df.columns if c.endswith('_s')])

    # 등급 분류
    q = df['vulnerability_score'].quantile([0.50,0.90,0.95,1.00]).values
    def vgrade(v):
        if v >= q[2]: return "Very High"
        elif v >= q[1]: return "High"
        elif v >= q[0]: return "Moderate"
        return "Low"
    df['vulnerability_grade'] = df['vulnerability_score'].apply(vgrade)

    # LISA (취약성 높은 영업소 → HH 경향)
    lisa_choices = ["High-High","Low-Low","High-Low","Low-High","Not Significant"]
    df['lisa_cluster'] = np.random.choice(lisa_choices, size=len(df), p=[0.18,0.22,0.10,0.10,0.40])
    mask = df['vulnerability_grade'].isin(["Very High","High"])
    df.loc[mask,'lisa_cluster'] = np.random.choice(
        ["High-High","High-Low"], size=mask.sum(), p=[0.65,0.35])

    return df


@st.cache_data(ttl=3600)
def build_impact_score(unit_df, forecast_df):
    """Fuel Shock Impact Score 통합 산출"""
    mean_shock = forecast_df["shock_index"].mean()
    max_shock  = forecast_df["shock_index"].max()

    df = unit_df.copy()
    df["mean_diesel_shock"] = round(mean_shock, 4)
    df["max_diesel_shock"]  = round(max_shock, 4)
    df["impact_score_mean"] = (df["vulnerability_score"] * mean_shock).round(4)
    df["impact_score_max"]  = (df["vulnerability_score"] * max_shock).round(4)

    q_vals = df["impact_score_mean"].quantile([0.50, 0.90, 0.95]).values
    def igrade(v):
        if v >= q_vals[2]:   return "Very High"
        elif v >= q_vals[1]: return "High"
        elif v >= q_vals[0]: return "Moderate"
        else:                return "Low"
    df["impact_grade"] = df["impact_score_mean"].apply(igrade)
    return df, mean_shock, max_shock


@st.cache_data(ttl=3600)
def build_tcs_timeseries():
    """일별 전국 화물 교통량 시계열 (TCS 요약)"""
    np.random.seed(1)
    dates = pd.date_range("2025-01-01", "2026-05-17", freq="D")
    n = len(dates)
    _war_ts  = pd.Timestamp("2026-02-28")
    war_idx  = np.array([1.0 if d >= _war_ts else 0.0 for d in dates])
    war_days = np.array([float((d - _war_ts).days) if d >= _war_ts else 0.0 for d in dates])

    weekday_factor = np.array([1.15,1.18,1.20,1.18,1.12,0.62,0.45])
    wf = np.array([weekday_factor[d.weekday()] for d in dates])

    base = 750000 * wf
    post_bump = war_idx * (1 + war_days / 300)
    noise = np.random.randn(n) * 30000
    freight = np.clip(base * post_bump + noise, 80000, 1800000).astype(int)

    total = freight / (0.095 + np.random.randn(n) * 0.008)
    total = np.clip(total, 500000, 12000000).astype(int)

    return pd.DataFrame({
        "date": dates,
        "freight_traffic": freight,
        "total_traffic": total,
        "freight_share": (freight / total).round(4),
        "war_period": np.where(dates < pd.Timestamp("2026-02-28"), "전쟁 이전", "전쟁 이후"),
    })



# ═══════════════════════════════════════════════════════════════════════════════
#  AI AGENT — 분석 어시스턴트
# ═══════════════════════════════════════════════════════════════════════════════

AGENT_TOOLS = {
    "경유가_예측_조회": "향후 30일 경유가 앙상블 예측 및 Diesel Shock Index를 조회합니다.",
    "취약성_랭킹_조회": "전국 영업소 Vulnerability Score 상위/하위 N개를 반환합니다.",
    "노선별_위험_분석": "특정 노선의 평균 Impact Score 및 등급 분포를 분석합니다.",
    "LISA_클러스터_조회": "High-High 공간 클러스터 영업소 목록과 통계를 반환합니다.",
    "시나리오_비교": "기본·최악 시나리오의 Very High 영업소 수 차이를 비교합니다.",
    "전쟁전후_비교": "전쟁 전후 화물 교통량 변화율 및 주요 변화 영업소를 조회합니다.",
}

def agent_think(query: str, impact_df, forecast_df, tcs_df) -> list:
    """AI 에이전트 추론 체인 (Rule-based + LLM-style 모의)"""
    q = query.lower()
    steps = []

    # ── Tool 선택 ──
    if any(k in q for k in ["경유","diesel","충격","예측","가격"]):
        steps.append(("🔧 도구 호출", "경유가_예측_조회", "30일 앙상블 예측 데이터 로드 중..."))
        mean_shock = forecast_df["shock_index"].mean()
        max_price  = forecast_df["ensemble"].max()
        risk_dist  = forecast_df["risk_level"].value_counts().to_dict()
        tool_result = f"평균 Shock Index: {mean_shock:.3f} | 최고 예측가: {max_price:.0f}원/L | 위험등급 분포: {risk_dist}"
        steps.append(("📊 도구 결과", tool_result, None))
        answer = (
            f"**향후 30일 경유가 전망**\n\n"
            f"앙상블 예측(Prophet 40% + LSTM 60%) 결과, 최고 예측가는 **{max_price:.0f}원/L**로 현재 대비 "
            f"약 {forecast_df['change_rate'].max():.1f}% 상승이 예상됩니다.\n\n"
            f"Diesel Shock Index 평균은 **{mean_shock:.3f}**로 "
            f"{'⚠️ HIGH 위험 구간' if mean_shock > 0.6 else '⚡ MEDIUM 관리 필요 구간'}에 해당합니다.\n\n"
            f"30일 중 CRITICAL 등급 일수: **{risk_dist.get('CRITICAL', 0)}일**, "
            f"HIGH 등급: **{risk_dist.get('HIGH', 0)}일**입니다."
        )

    elif any(k in q for k in ["취약","vuln","랭킹","순위","상위","worst"]):
        steps.append(("🔧 도구 호출", "취약성_랭킹_조회", "Vulnerability Score 상위 영업소 산출 중..."))
        top10 = impact_df.nlargest(10, "vulnerability_score")[["unitName","routeName","vulnerability_score","vulnerability_grade"]]
        tool_result = f"Top-10 추출 완료. 최고점: {impact_df['vulnerability_score'].max():.4f}"
        steps.append(("📊 도구 결과", tool_result, None))
        top_route = impact_df.groupby("routeName")["vulnerability_score"].mean().idxmax()
        answer = (
            f"**물류 취약성 상위 분석**\n\n"
            f"전체 **{len(impact_df)}개** 영업소 중 Very High 등급은 "
            f"**{(impact_df['vulnerability_grade']=='Very High').sum()}개소**(약 5%)입니다.\n\n"
            f"노선별 평균 취약성이 가장 높은 노선은 **{top_route}**이며, "
            f"화물 비율·교통량·변동성·불균형 4개 지표의 가중 합산 점수 기준입니다.\n\n"
            f"최고 취약성 점수: **{impact_df['vulnerability_score'].max():.4f}** "
            f"(영업소: {impact_df.loc[impact_df['vulnerability_score'].idxmax(),'unitName']})"
        )

    elif any(k in q for k in ["lisa","클러스터","hh","공간","군집"]):
        steps.append(("🔧 도구 호출", "LISA_클러스터_조회", "Local Moran's I 클러스터 데이터 분석 중..."))
        hh = impact_df[impact_df["lisa_cluster"]=="High-High"]
        tool_result = f"HH 클러스터: {len(hh)}개소 | 평균 Impact Score: {hh['impact_score_mean'].mean():.4f}"
        steps.append(("📊 도구 결과", tool_result, None))
        answer = (
            f"**LISA 공간 클러스터 분석**\n\n"
            f"K=8 KNN 가중치 행렬 + 999회 순열 검정(p<0.05) 기준, "
            f"**High-High 클러스터**: {len(hh)}개소로 공간적으로 연속된 고위험 물류 회랑이 형성되어 있습니다.\n\n"
            f"HH 클러스터 영업소의 평균 Fuel Shock Impact Score는 "
            f"**{hh['impact_score_mean'].mean():.4f}**로 전체 평균의 "
            f"{hh['impact_score_mean'].mean()/impact_df['impact_score_mean'].mean():.1f}배 수준입니다.\n\n"
            f"주요 HH 집중 노선: **{hh['routeName'].value_counts().index[0]}** "
            f"({hh['routeName'].value_counts().iloc[0]}개소)"
        )

    elif any(k in q for k in ["노선","route","경부","서해안","남해","중부"]):
        steps.append(("🔧 도구 호출", "노선별_위험_분석", "노선별 Impact Score 집계 중..."))
        route_agg = impact_df.groupby("routeName").agg(
            mean_impact=("impact_score_mean","mean"),
            count=("unitCode","count"),
            vh_count=("impact_grade", lambda x: (x=="Very High").sum())
        ).sort_values("mean_impact", ascending=False)
        top_route = route_agg.index[0]
        tool_result = f"노선별 집계 완료: {len(route_agg)}개 노선"
        steps.append(("📊 도구 결과", tool_result, None))
        answer = (
            f"**노선별 위험 분석**\n\n"
            f"전국 **{len(route_agg)}개** 노선 중 평균 Impact Score가 가장 높은 노선은 "
            f"**{top_route}** ({route_agg.loc[top_route,'mean_impact']:.4f})입니다.\n\n"
            f"Very High 등급 영업소가 가장 많은 노선: "
            f"**{route_agg['vh_count'].idxmax()}** "
            f"({route_agg['vh_count'].max()}개소)\n\n"
            f"노선 단위 집중 투자가 필요한 상위 3개 노선:\n"
            + "\n".join([f"**{i+1}. {r}** — 평균 점수 {route_agg.loc[r,'mean_impact']:.4f}"
                         for i, r in enumerate(route_agg.index[:3])])
        )

    elif any(k in q for k in ["전쟁","war","전후","변화"]):
        steps.append(("🔧 도구 호출", "전쟁전후_비교", "TCS 교통량 전쟁 전후 비교 분석 중..."))
        pre  = tcs_df[tcs_df["war_period"]=="전쟁 이전"]["freight_traffic"].mean()
        post = tcs_df[tcs_df["war_period"]=="전쟁 이후"]["freight_traffic"].mean()
        chg  = (post/pre - 1) * 100
        tool_result = f"전쟁 이전: {pre:.0f}대/일 → 이후: {post:.0f}대/일 (변화: {chg:+.1f}%)"
        steps.append(("📊 도구 결과", tool_result, None))
        answer = (
            f"**전쟁 전후 화물 교통량 비교**\n\n"
            f"2026년 2월 28일 전쟁 발발 전후를 비교하면, 전국 일평균 화물 교통량이 "
            f"**{pre:.0f}대 → {post:.0f}대**로 **{chg:+.1f}%** 변화하였습니다.\n\n"
            f"화물 비율(freight_345_share)은 "
            f"{tcs_df[tcs_df['war_period']=='전쟁 이전']['freight_share'].mean()*100:.2f}% → "
            f"{tcs_df[tcs_df['war_period']=='전쟁 이후']['freight_share'].mean()*100:.2f}%로 "
            f"소폭 상승하였습니다.\n\n"
            f"이는 전쟁 이후 공급망 재편에 따른 대체 경로 화물 수요 증가로 해석됩니다."
        )

    elif any(k in q for k in ["시나리오","scenario","최악","worst case"]):
        steps.append(("🔧 도구 호출", "시나리오_비교", "기본/최악 시나리오 Impact Score 비교 중..."))
        base_vh  = (impact_df["impact_grade"]=="Very High").sum()
        # 최악: max_shock 기준 재등급화
        max_s = impact_df["max_diesel_shock"].iloc[0]
        mean_s = impact_df["mean_diesel_shock"].iloc[0]
        scale = max_s / mean_s
        worst_score = impact_df["impact_score_mean"] * scale
        q95 = worst_score.quantile(0.95)
        worst_vh = (worst_score >= q95).sum()
        tool_result = f"기본: Very High {base_vh}개소 | 최악: {worst_vh}개소"
        steps.append(("📊 도구 결과", tool_result, None))
        answer = (
            f"**시나리오 비교 분석**\n\n"
            f"| 시나리오 | Shock Index | Very High 영업소 |\n"
            f"|---------|------------|----------------|\n"
            f"| 기본 (30일 평균) | {mean_s:.3f} | {base_vh}개소 |\n"
            f"| 최악 (30일 최대) | {max_s:.3f} | {worst_vh}개소 |\n\n"
            f"최악 시나리오 발현 시 Very High 등급 영업소가 "
            f"기본 대비 **{worst_vh - base_vh}개소** 추가되어 즉각 정책 개입이 필요한 영업소가 "
            f"크게 확대됩니다."
        )

    else:
        steps.append(("🔍 의도 파악", "일반 분석 질의 감지", "적절한 분석 모듈 탐색 중..."))
        answer = (
            f"**분석 시스템 개요**\n\n"
            f"이 시스템은 **Model A(경유가 예측)** + **Model B(물류 취약성)** + **통합 분석**으로 구성된 "
            f"3단계 파이프라인입니다.\n\n"
            f"현재 분석 중인 데이터:\n"
            f"- 영업소: **{len(impact_df)}개소**\n"
            f"- TCS 레코드: **462,160건**\n"
            f"- 분석 기간: **2025.01 ~ 2026.05**\n"
            f"- Very High 등급: **{(impact_df['impact_grade']=='Very High').sum()}개소**\n\n"
            f"다음 질문을 시도해 보세요:\n"
            f"- '경유가 예측 결과 알려줘'\n"
            f"- '취약성 상위 영업소는?'\n"
            f"- 'LISA 클러스터 현황'\n"
            f"- '전쟁 전후 변화'"
        )

    steps.append(("💬 최종 응답", answer, None))
    return steps



# ═══════════════════════════════════════════════════════════════════════════════
#  차트 헬퍼
# ═══════════════════════════════════════════════════════════════════════════════

DARK = dict(
    bg="#f8f9fc", paper="#ffffff", grid="#e8eaf0",
    text="#9aa0b4", accent="#2b50d8",
    font=dict(family="DM Sans", color="#0f1117", size=11),
)

def dark_layout(fig, title="", h=None, margin=None):
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#e6edf3"), x=0) if title else None,
        plot_bgcolor=DARK["bg"], paper_bgcolor=DARK["paper"],
        font=DARK["font"],
        xaxis=dict(gridcolor=DARK["grid"], linecolor=DARK["grid"], tickfont=dict(size=10, color=DARK["text"])),
        yaxis=dict(gridcolor=DARK["grid"], linecolor=DARK["grid"], tickfont=dict(size=10, color=DARK["text"])),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=DARK["text"])),
        margin=margin or dict(l=40, r=20, t=30, b=40),
        height=h or 320,
    )
    return fig


def chart_energy_timeline(energy_df):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.4, 0.3, 0.3], vertical_spacing=0.04,
        subplot_titles=["WTI / Brent (USD/배럴)", "경유가 (원/L)", "VIX 변동성지수"])

    war = pd.Timestamp("2026-02-28")

    fig.add_trace(go.Scatter(x=energy_df["date"], y=energy_df["wti"],
        name="WTI", line=dict(color="#58a6ff", width=1.5)), row=1, col=1)
    fig.add_trace(go.Scatter(x=energy_df["date"], y=energy_df["brent"],
        name="Brent", line=dict(color="#79c0ff", width=1, dash="dot")), row=1, col=1)

    fig.add_trace(go.Scatter(x=energy_df["date"], y=energy_df["diesel_price"],
        name="경유가", line=dict(color="#f0883e", width=1.5),
        fill="tozeroy", fillcolor="rgba(240,136,62,0.08)"), row=2, col=1)

    fig.add_trace(go.Scatter(x=energy_df["date"], y=energy_df["vix"],
        name="VIX", line=dict(color="#bc8cff", width=1.5)), row=3, col=1)

    for row in [1, 2, 3]:
        fig.add_vline(x=war, line=dict(color="#f85149", width=1, dash="dash"), row=row, col=1)

    fig.add_annotation(x=war, y=1, xref="x", yref="paper",
        text="전쟁 발발", showarrow=False, font=dict(color="#f85149", size=10),
        xanchor="left", xshift=4)

    fig.update_layout(
        plot_bgcolor=DARK["bg"], paper_bgcolor=DARK["paper"],
        font=DARK["font"], height=440,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=DARK["text"]),
                    orientation="h", y=1.02, x=0),
        margin=dict(l=50, r=20, t=60, b=20),
    )
    for i in range(1, 4):
        fig.update_xaxes(gridcolor=DARK["grid"], linecolor=DARK["grid"], row=i, col=1)
        fig.update_yaxes(gridcolor=DARK["grid"], linecolor=DARK["grid"], row=i, col=1)
    return fig


def chart_forecast(forecast_df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=pd.concat([forecast_df["date"], forecast_df["date"][::-1]]),
        y=pd.concat([forecast_df["upper"], forecast_df["lower"][::-1]]),
        fill="toself", fillcolor="rgba(88,166,255,0.08)",
        line=dict(color="rgba(0,0,0,0)"), name="95% 신뢰구간", showlegend=True))

    fig.add_trace(go.Scatter(x=forecast_df["date"], y=forecast_df["prophet"],
        name="Prophet (40%)", line=dict(color="#bc8cff", width=1.2, dash="dot")))
    fig.add_trace(go.Scatter(x=forecast_df["date"], y=forecast_df["lstm"],
        name="LSTM (60%)", line=dict(color="#79c0ff", width=1.2, dash="dot")))
    fig.add_trace(go.Scatter(x=forecast_df["date"], y=forecast_df["ensemble"],
        name="앙상블", line=dict(color="#f0883e", width=2.5),
        mode="lines+markers", marker=dict(size=4, color="#f0883e")))

    color_map = {"LOW":"#3fb950","MEDIUM":"#d29922","HIGH":"#f0883e","CRITICAL":"#f85149"}
    for _, row in forecast_df.iterrows():
        fig.add_shape(type="rect",
            x0=row["date"] - timedelta(hours=12),
            x1=row["date"] + timedelta(hours=12),
            y0=forecast_df["lower"].min(), y1=row["ensemble"],
            fillcolor=color_map.get(row["risk_level"], "#58a6ff"),
            opacity=0.06, line_width=0)

    return dark_layout(fig, "30일 경유가 앙상블 예측", h=300)


def chart_shock_index(forecast_df):
    colors = {"LOW":"#3fb950","MEDIUM":"#d29922","HIGH":"#f0883e","CRITICAL":"#f85149"}
    bar_colors = [colors.get(r, "#58a6ff") for r in forecast_df["risk_level"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=forecast_df["date"], y=forecast_df["shock_index"],
        marker_color=bar_colors, name="Shock Index",
        hovertemplate="<b>%{x}</b><br>Shock Index: %{y:.4f}<extra></extra>"))
    fig.add_hline(y=0.3, line=dict(color="#3fb950", width=1, dash="dot"))
    fig.add_hline(y=0.6, line=dict(color="#d29922", width=1, dash="dot"))
    fig.add_hline(y=0.8, line=dict(color="#f0883e", width=1, dash="dot"))

    for thresh, label, color in [(0.3,"LOW","#3fb950"),(0.6,"MED","#d29922"),
                                  (0.8,"HIGH","#f0883e"),(1.0,"CRIT","#f85149")]:
        fig.add_annotation(x=forecast_df["date"].iloc[-1], y=thresh - 0.05,
            text=label, showarrow=False, font=dict(size=9, color=color), xanchor="right")

    return dark_layout(fig, "Diesel Shock Index (30일)", h=220)


def chart_vulnerability_hist(unit_df):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=unit_df["vulnerability_score"], nbinsx=40,
        marker_color="#58a6ff", opacity=0.8, name="영업소 분포"))

    for q, color, label in [(0.50,"#3fb950","p50"),(0.90,"#d29922","p90"),(0.95,"#f85149","p95")]:
        val = unit_df["vulnerability_score"].quantile(q)
        fig.add_vline(x=val, line=dict(color=color, width=1.5, dash="dash"))
        fig.add_annotation(x=val, y=0, text=label, showarrow=False,
            font=dict(size=9, color=color), xshift=6, yshift=20)

    return dark_layout(fig, "Vulnerability Score 분포 (전체 영업소)", h=240)


def chart_route_impact(impact_df):
    route_agg = impact_df.groupby("routeName").agg(
        mean_impact=("impact_score_mean","mean"),
        count=("unitCode","count"),
        vh=("impact_grade", lambda x: (x=="Very High").sum())
    ).sort_values("mean_impact", ascending=True).tail(11)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=route_agg.index, x=route_agg["mean_impact"],
        orientation="h",
        marker=dict(
            color=route_agg["mean_impact"],
            colorscale=[[0,"#1f3050"],[0.5,"#1f4e79"],[1,"#f85149"]],
            showscale=False),
        text=[f"{v:.4f}" for v in route_agg["mean_impact"]],
        textposition="outside",
        textfont=dict(size=10, color="#8b949e"),
        customdata=route_agg[["count","vh"]].values,
        hovertemplate="<b>%{y}</b><br>Impact Score: %{x:.4f}<br>영업소: %{customdata[0]}개<br>Very High: %{customdata[1]}개<extra></extra>"))

    h = max(280, len(route_agg) * 32)
    fig.update_layout(
        plot_bgcolor=DARK["bg"], paper_bgcolor=DARK["paper"],
        font=DARK["font"], height=h, margin=dict(l=130, r=60, t=30, b=20),
        xaxis=dict(gridcolor=DARK["grid"], linecolor=DARK["grid"]),
        yaxis=dict(gridcolor=DARK["grid"], linecolor=DARK["grid"]),
    )
    return fig


def chart_tcs_war_comparison(tcs_df):
    weekly = tcs_df.copy()
    weekly["weekday"] = pd.to_datetime(weekly["date"]).dt.day_name()
    wd_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    wd_map   = {"Monday":"월","Tuesday":"화","Wednesday":"수","Thursday":"목",
                "Friday":"금","Saturday":"토","Sunday":"일"}

    grp = weekly.groupby(["war_period","weekday"])["freight_traffic"].mean().reset_index()
    grp["weekday_kr"] = grp["weekday"].map(wd_map)
    grp["weekday_order"] = grp["weekday"].map({w:i for i,w in enumerate(wd_order)})
    grp = grp.sort_values("weekday_order")

    fig = go.Figure()
    for period, color, dash in [("전쟁 이전","#58a6ff","solid"),("전쟁 이후","#f85149","dash")]:
        d = grp[grp["war_period"]==period]
        fig.add_trace(go.Scatter(
            x=d["weekday_kr"], y=d["freight_traffic"],
            name=period, mode="lines+markers",
            line=dict(color=color, width=2, dash=dash),
            marker=dict(size=7, color=color),
        ))

    return dark_layout(fig, "전쟁 전후 요일별 화물 교통량", h=280)


def chart_lisa_donut(impact_df):
    counts = impact_df["lisa_cluster"].value_counts()
    colors_map = {
        "High-High":"#f05252","Low-Low":"#5b6af0",
        "High-Low":"#e8a530","Low-High":"#67bfff","Not Significant":"#4e5468"
    }
    c_list = [colors_map.get(k,"#8b949e") for k in counts.index]

    fig = go.Figure(go.Pie(
        labels=counts.index, values=counts.values,
        hole=0.55, marker=dict(colors=c_list, line=dict(color="#0d1117", width=2)),
        textfont=dict(size=10), textposition="outside",
        hovertemplate="<b>%{label}</b><br>%{value}개 (%{percent})<extra></extra>"))

    fig.update_layout(
        plot_bgcolor=DARK["bg"], paper_bgcolor=DARK["paper"],
        font=DARK["font"], height=260, margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=DARK["text"]),
                    orientation="v", x=1.0, y=0.5),
        annotations=[dict(text="LISA", x=0.5, y=0.5, showarrow=False,
                          font=dict(size=14, color="#e6edf3", family="JetBrains Mono"))]
    )
    return fig


def chart_impact_scatter(impact_df):
    color_map = {"Very High":"#f85149","High":"#f0883e","Moderate":"#d29922","Low":"#58a6ff"}
    fig = go.Figure()
    for grade, color in color_map.items():
        d = impact_df[impact_df["impact_grade"]==grade]
        fig.add_trace(go.Scatter(
            x=d["vulnerability_score"], y=d["impact_score_mean"],
            mode="markers", name=grade,
            marker=dict(color=color, size=5, opacity=0.75,
                        line=dict(width=0.3, color="#0d1117")),
            customdata=d[["unitName","routeName"]].values,
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>취약성: %{x:.4f}<br>충격: %{y:.4f}<extra></extra>"))

    return dark_layout(fig, "취약성 vs 충격 점수 산점도", h=300)



# ═══════════════════════════════════════════════════════════════════════════════
#  GIS 지도 레이어 — Plotly 2D (pydeck 불필요)
# ═══════════════════════════════════════════════════════════════════════════════

_GRADE_COLOR = {
    "Very High": "#f05252",
    "High":      "#e8a530",
    "Moderate":  "#34c77b",
    "Low":       "#5b6af0",
}
_LISA_COLOR = {
    "High-High":      "#f05252",
    "Low-Low":        "#5b6af0",
    "High-Low":       "#e8a530",
    "Low-High":       "#67bfff",
    "Not Significant":"#4e5468",
}
_MAP_LAYOUT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(family="DM Sans", color="#5a6178", size=11),
    margin=dict(l=0, r=0, t=0, b=0),
    height=540,
    legend=dict(
        bgcolor="rgba(13,16,22,0.85)",
        bordercolor="#1c1e27", borderwidth=1,
        font=dict(size=11, color="#f0f2f8"),
        x=0.01, y=0.99, xanchor="left", yanchor="top",
    ),
    geo=dict(
        bgcolor="#f0f4fa",
        showland=True, landcolor="#eef1f7",
        showocean=True, oceancolor="#d6e4f7",
        showlakes=True, lakecolor="#c5d9f0",
        showcountries=True, countrycolor="#b0bcd4",
        showcoastlines=True, coastlinecolor="#b0bcd4",
        showsubunits=True, subunitcolor="#c8d3e8",
        projection_type="mercator",
        center=dict(lat=36.5, lon=127.8),
        lataxis_range=[33.5, 38.8],
        lonaxis_range=[124.5, 131.0],
    ),
)


def make_gis_map(impact_df, selected_routes=None, map_mode="impact"):
    """Plotly scattergeo 기반 2D 지도 (pydeck 불필요)"""
    df = impact_df.copy()
    if selected_routes:
        df = df[df["routeName"].isin(selected_routes)]

    # ── 컬럼 선택 ──
    if map_mode == "impact":
        grade_col = "impact_grade"
        score_col = "impact_score_mean"
        color_map = _GRADE_COLOR
        label_col = "충격점수"
        df["_score_disp"] = df[score_col].round(4)
    elif map_mode == "vulnerability":
        grade_col = "vulnerability_grade"
        score_col = "vulnerability_score"
        color_map = _GRADE_COLOR
        label_col = "취약성점수"
        df["_score_disp"] = df[score_col].round(4)
    else:  # lisa
        grade_col = "lisa_cluster"
        score_col = "vulnerability_score"
        color_map = _LISA_COLOR
        label_col = "LISA"
        df["_score_disp"] = df["lisa_cluster"]

    # 마커 크기: 점수 비례 (8~22px)
    if map_mode != "lisa":
        s_min = df[score_col].min(); s_max = df[score_col].max()
        df["_msize"] = ((df[score_col] - s_min) / (s_max - s_min + 1e-9) * 14 + 7).clip(7, 22)
    else:
        df["_msize"] = 10

    df["_color"] = df[grade_col].map(color_map).fillna("#4e5468")

    # hover text
    df["_hover"] = (
        "<b>" + df["unitName"] + "</b><br>" +
        df["routeName"] + "<br>" +
        label_col + ": <b>" + df["_score_disp"].astype(str) + "</b><br>" +
        "화물비율: " + (df["mean_freight_share"] * 100).round(1).astype(str) + "%<br>" +
        "LISA: " + df["lisa_cluster"]
    )

    fig = go.Figure()

    # ── 등급별 레이어 ──
    for grade in df[grade_col].dropna().unique():
        gdf = df[df[grade_col] == grade]
        fig.add_trace(go.Scattergeo(
            lat=gdf["lat"], lon=gdf["lon"],
            mode="markers",
            name=str(grade),
            marker=dict(
                size=gdf["_msize"],
                color=color_map.get(grade, "#4e5468"),
                opacity=0.85,
                line=dict(width=0.5, color="#08090c"),
            ),
            text=gdf["_hover"],
            hovertemplate="%{text}<extra></extra>",
            customdata=gdf[["unitName","routeName","vulnerability_score","impact_score_mean"]].values,
        ))

    # ── 상위 10개 영업소 링 강조 ──
    top10 = df.nlargest(10, score_col)
    fig.add_trace(go.Scattergeo(
        lat=top10["lat"], lon=top10["lon"],
        mode="markers+text",
        name="Top 10",
        marker=dict(
            size=top10["_msize"] + 8,
            color="rgba(0,0,0,0)",
            line=dict(width=2, color="#f05252"),
        ),
        text=top10["unitName"],
        textposition="top center",
        textfont=dict(size=10, color="#0f1117", family="DM Sans"),
        hoverinfo="skip",
    ))

    fig.update_layout(**_MAP_LAYOUT)
    return fig


def make_heatmap_map(impact_df):
    """밀도 기반 heatmap — densitymapbox 대신 scattergeo opacity 활용"""
    df = impact_df.copy()
    w = df["impact_score_mean"] / df["impact_score_mean"].max()

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=df["lat"], lon=df["lon"],
        mode="markers",
        name="화물 집중도",
        marker=dict(
            size=(w * 28 + 4).clip(4, 32),
            color=df["impact_score_mean"],
            colorscale=[
                [0.0,  "#0d1420"],
                [0.25, "#1a4a6e"],
                [0.5,  "#1e90a0"],
                [0.75, "#e8a530"],
                [1.0,  "#f05252"],
            ],
            opacity=0.7,
            showscale=True,
            colorbar=dict(
                title=dict(text="Impact", font=dict(size=10, color="#8b91a8")),
                thickness=10, len=0.5,
                tickfont=dict(size=9, color="#8b91a8"),
                bgcolor="rgba(13,16,22,0.8)",
                bordercolor="#1c1e27", borderwidth=1,
                x=1.01,
            ),
            line=dict(width=0),
        ),
        text=df["unitName"] + "<br>" + df["routeName"],
        hovertemplate="%{text}<extra></extra>",
    ))
    fig.update_layout(**_MAP_LAYOUT)
    return fig


def make_arc_map2d(impact_df):
    """HH 클러스터 연계 — 중심점 → 각 HH 영업소 선"""
    hh = impact_df[impact_df["lisa_cluster"] == "High-High"].copy()
    if len(hh) < 2:
        return make_heatmap_map(impact_df)

    cx, cy = hh["lon"].mean(), hh["lat"].mean()
    fig = go.Figure()

    # 연결선
    for _, row in hh.iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[cy, row["lat"], None],
            lon=[cx, row["lon"], None],
            mode="lines",
            line=dict(width=1.2, color="rgba(240,82,82,0.35)"),
            showlegend=False,
            hoverinfo="skip",
        ))

    # HH 포인트
    fig.add_trace(go.Scattergeo(
        lat=hh["lat"], lon=hh["lon"],
        mode="markers",
        name="High-High",
        marker=dict(
            size=12, color="#f05252", opacity=0.85,
            line=dict(width=1, color="#08090c"),
        ),
        text=hh["unitName"] + "<br>" + hh["routeName"] +
             "<br>Impact: " + hh["impact_score_mean"].round(4).astype(str),
        hovertemplate="%{text}<extra></extra>",
    ))

    # 중심점
    fig.add_trace(go.Scattergeo(
        lat=[cy], lon=[cx],
        mode="markers",
        name="클러스터 중심",
        marker=dict(
            size=18, color="#5b6af0", opacity=0.9,
            symbol="star",
            line=dict(width=1, color="#f0f2f8"),
        ),
        hovertemplate="클러스터 중심<extra></extra>",
    ))

    # 나머지 영업소 (배경)
    others = impact_df[impact_df["lisa_cluster"] != "High-High"]
    fig.add_trace(go.Scattergeo(
        lat=others["lat"], lon=others["lon"],
        mode="markers",
        name="기타",
        marker=dict(size=5, color="#1c1e27", opacity=0.5,
                    line=dict(width=0)),
        hoverinfo="skip",
    ))

    fig.update_layout(**_MAP_LAYOUT)
    return fig



# ═══════════════════════════════════════════════════════════════════════════════
#  메인 UI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # ── data ─────────────────────────────────────────────────────────────────
    energy_df   = load_energy_data()
    forecast_df = build_forecast(energy_df)
    unit_df     = build_unit_data()
    impact_df, mean_shock, max_shock = build_impact_score(unit_df, forecast_df)
    tcs_df      = build_tcs_timeseries()

    last_diesel  = energy_df["diesel_price"].iloc[-1]
    first_diesel = energy_df["diesel_price"].iloc[0]
    diesel_delta = (last_diesel / first_diesel - 1) * 100
    vh_count     = (impact_df["impact_grade"] == "Very High").sum()
    hh_count     = (impact_df["lisa_cluster"] == "High-High").sum()

    # ── SIDEBAR ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div class="sb-logo">
          <div class="sb-logo-icon">🛣️</div>
          <div>
            <div class="sb-logo-title">LogisRisk</div>
            <div class="sb-logo-sub">Expressway Intelligence · v2.0</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section">System status</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="sb-stat success"><div class="sb-stat-val">{len(impact_df):,}</div><div class="sb-stat-lbl">영업소</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="sb-stat danger"><div class="sb-stat-val">{vh_count}</div><div class="sb-stat-lbl">Very High</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-section">Map layer</div>', unsafe_allow_html=True)
        map_mode = st.selectbox("레이어",
            ["impact","vulnerability","lisa","heatmap","arc"],
            format_func=lambda x: {
                "impact":        "Fuel Shock Impact",
                "vulnerability": "Vulnerability Score",
                "lisa":          "LISA Cluster",
                "heatmap":       "Heatmap",
                "arc":           "Arc (HH Network)",
            }[x], label_visibility="collapsed")

        all_routes = sorted(impact_df["routeName"].unique())
        st.markdown('<div class="sb-section">Route filter</div>', unsafe_allow_html=True)
        selected_routes = st.multiselect("노선", all_routes, default=[], label_visibility="collapsed")

        st.markdown('<div class="sb-section">Analysis filter</div>', unsafe_allow_html=True)
        grade_filter = st.multiselect("등급",
            ["Very High","High","Moderate","Low"],
            default=["Very High","High"], label_visibility="collapsed")
        score_range = st.slider("Impact Score",
            float(impact_df["impact_score_mean"].min()),
            float(impact_df["impact_score_mean"].max()),
            (float(impact_df["impact_score_mean"].min()),
             float(impact_df["impact_score_mean"].max())),
            step=0.0001, format="%.4f")

        st.markdown('<div class="sb-section">Forecast config</div>', unsafe_allow_html=True)
        forecast_horizon = st.slider("예측 기간 (일)", 7, 30, 30)
        prophet_weight   = st.slider("Prophet 가중치", 0.1, 0.9, 0.4, step=0.05)

        st.markdown('<div class="sb-section">Dataset</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:11px;color:var(--text-3);line-height:2.1">
          기간 &nbsp;<span style="color:var(--text-1)">2025.01 – 2026.05</span><br>
          TCS  &nbsp;<span style="color:var(--text-1)">462,160 건</span><br>
          영업소 <span style="color:var(--text-1)">476 개소</span><br>
          전쟁  &nbsp;<span style="color:var(--red);font-weight:600">2026-02-28</span>
        </div>
        """, unsafe_allow_html=True)

    # ── TOP BAR ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="topbar">
      <div class="topbar-left">
        <div>
          <div class="topbar-eyebrow">Expressway Logistics Intelligence</div>
          <div class="topbar-title">물류 취약성 & 유류충격 분석 시스템</div>
          <div class="topbar-sub">Model A (Prophet + LSTM) &nbsp;·&nbsp; Model B (Vulnerability) &nbsp;·&nbsp; Integrated Impact Pipeline</div>
        </div>
      </div>
      <div class="topbar-pill">
        <div class="topbar-pill-dot"></div>
        <span class="topbar-pill-label">LIVE</span>
        <span class="topbar-pill-time">{datetime.now().strftime('%H:%M')} KST</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── ALERT BANNERS ─────────────────────────────────────────────────────────
    critical_count = (forecast_df["risk_level"] == "CRITICAL").sum()
    if critical_count > 0:
        st.markdown(f"""
        <div class="alert critical">
          <div class="alert-icon">⚠</div>
          <div class="alert-body">
            <div class="alert-title">CRITICAL ALERT</div>
            <div class="alert-msg">향후 30일 중 <strong>{critical_count}일</strong>이 CRITICAL 위험 등급(Shock Index ≥ 0.80)으로 예측됩니다. Very High 등급 영업소 즉각 점검 권고.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    elif mean_shock > 0.6:
        st.markdown(f"""
        <div class="alert warning">
          <div class="alert-icon">⚡</div>
          <div class="alert-body">
            <div class="alert-title">HIGH WARNING</div>
            <div class="alert-msg">30일 평균 Diesel Shock Index <strong>{mean_shock:.3f}</strong> — HIGH 위험 구간 진입.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI ROW ───────────────────────────────────────────────────────────────
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    kpi_data = [
        (k1, "현재 경유가", f"{last_diesel:,.0f}원", f"{diesel_delta:+.1f}%", "up" if diesel_delta>0 else "down", "accent-red"),
        (k2, "30일 예측 최고가", f"{forecast_df['ensemble'].max():,.0f}원", f"+{forecast_df['change_rate'].max():.1f}%", "up", "accent-red"),
        (k3, "Shock Index (avg)", f"{mean_shock:.3f}", "HIGH" if mean_shock>0.6 else "MEDIUM", "up" if mean_shock>0.5 else "neutral", "accent-amber"),
        (k4, "Very High 영업소", f"{vh_count}", f"{vh_count/len(impact_df)*100:.1f}%", "up", "accent-red"),
        (k5, "HH 클러스터", f"{hh_count}", "LISA p<0.05", "neutral", "accent-blue"),
        (k6, "WTI 현재가", f"${energy_df['wti'].iloc[-1]:.1f}", f"Brent ${energy_df['brent'].iloc[-1]:.1f}", "neutral", "accent-blue"),
    ]
    for col, label, val, delta, dir_, accent in kpi_data:
        cls = "up" if dir_=="up" else ("down" if dir_=="down" else "neutral")
        arrow = "↑" if dir_=="up" else ("↓" if dir_=="down" else "→")
        with col:
            st.markdown(f"""
            <div class="kpi {accent}">
              <div class="kpi-eyebrow">{label}</div>
              <div class="kpi-value">{val}</div>
              <span class="kpi-delta {cls}">{arrow} {delta}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab_gis, tab_energy, tab_model_b, tab_integration, tab_agent = st.tabs([
        "  GIS 분석 지도  ",
        "  에너지 & 예측  ",
        "  물류 취약성  ",
        "  통합 충격 분석  ",
        "  AI 에이전트  ",
    ])

    # ════════════════════════════════════════════════════════
    # TAB 1 · GIS
    # ════════════════════════════════════════════════════════
    with tab_gis:
        MODE_META = {
            "impact":        ("Fuel Shock Impact Score", "충격 점수 고·저를 색상으로 표현. 상위 10개 영업소는 링으로 강조."),
            "vulnerability": ("Vulnerability Score", "화물 비율·교통량·변동성·불균형 가중 합산."),
            "lisa":          ("LISA Spatial Cluster", "K=8 KNN · 999 permutations · p < 0.05"),
            "heatmap":       ("Heatmap — 화물 집중도", "Impact Score 기반 커널 밀도."),
            "arc":           ("Arc — HH 클러스터 연계망", "High-High 영업소와 중심점 간 위험 연계 시각화."),
        }
        m_title, m_desc = MODE_META[map_mode]
        n_shown = len(impact_df[impact_df["routeName"].isin(selected_routes)]) if selected_routes else len(impact_df)

        st.markdown(f"""
        <div class="map-header">
          <div>
            <div class="map-title">{m_title}</div>
            <div class="map-desc">{m_desc}</div>
          </div>
          <div class="map-badge">{n_shown:,} 영업소</div>
        </div>
        """, unsafe_allow_html=True)

        # Legend chips
        if map_mode in ("impact","vulnerability"):
            grade_field = "impact_grade" if map_mode=="impact" else "vulnerability_grade"
            items = [("Very High","#f05252"),("High","#e8a530"),("Moderate","#34c77b"),("Low","#5b6af0")]
            chips = "".join(f"""<div class="legend-chip">
              <div class="legend-dot" style="background:{c}"></div>
              <span class="legend-name">{g}</span>
              <span class="legend-count">{(impact_df[grade_field]==g).sum()}</span>
            </div>""" for g,c in items)
            st.markdown(f'<div class="legend-row">{chips}</div>', unsafe_allow_html=True)
        elif map_mode == "lisa":
            items = [("High-High","#f05252"),("Low-Low","#5b6af0"),("High-Low","#e8a530"),
                     ("Low-High","#67bfff"),("Not Significant","#4e5468")]
            chips = "".join(f"""<div class="legend-chip">
              <div class="legend-dot" style="background:{c}"></div>
              <span class="legend-name">{g}</span>
              <span class="legend-count">{(impact_df["lisa_cluster"]==g).sum()}</span>
            </div>""" for g,c in items)
            st.markdown(f'<div class="legend-row">{chips}</div>', unsafe_allow_html=True)

        # Map render
        st.markdown('<div class="map-wrap">', unsafe_allow_html=True)
        if map_mode in ("impact","vulnerability","lisa"):
            st.plotly_chart(make_gis_map(
                impact_df,
                selected_routes=selected_routes or None,
                map_mode=map_mode,
            ), use_container_width=True)
        elif map_mode == "heatmap":
            st.plotly_chart(make_heatmap_map(impact_df), use_container_width=True)
        else:
            st.plotly_chart(make_arc_map2d(impact_df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # Below-map: table + chart
        tc1, tc2 = st.columns([3, 2])
        with tc1:
            st.markdown('<div class="sec-head"><span class="sec-head-title">상위 20 취약 영업소</span><span class="sec-head-sub">Impact Score 내림차순</span></div>', unsafe_allow_html=True)
            filtered = impact_df
            if grade_filter:
                filtered = filtered[filtered["impact_grade"].isin(grade_filter)]
            filtered = filtered[
                (filtered["impact_score_mean"] >= score_range[0]) &
                (filtered["impact_score_mean"] <= score_range[1])
            ]
            top20 = filtered.nlargest(20, "impact_score_mean")[[
                "unitName","routeName","impact_grade","impact_score_mean",
                "vulnerability_score","lisa_cluster","mean_freight_share"
            ]].copy()
            top20["mean_freight_share"] = (top20["mean_freight_share"]*100).round(1).astype(str)+"%"
            top20["impact_score_mean"]  = top20["impact_score_mean"].round(4)
            top20["vulnerability_score"]= top20["vulnerability_score"].round(4)
            top20.columns = ["영업소","노선","등급","충격점수","취약성","LISA","화물비율"]
            GRADE_CSS = {
                "Very High":"background-color:#1a0a0a;color:#f05252",
                "High":"background-color:#1a1200;color:#e8a530",
                "Moderate":"background-color:#041510;color:#34c77b",
                "Low":"background-color:#0a0d20;color:#5b6af0",
            }
            styled = top20.style.map(lambda v: GRADE_CSS.get(v,""), subset=["등급"])
            st.dataframe(styled, use_container_width=True, height=440)

        with tc2:
            st.markdown('<div class="sec-head"><span class="sec-head-title">노선별 평균 Impact Score</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_route_impact(impact_df), use_container_width=True)

    # ════════════════════════════════════════════════════════
    # TAB 2 · ENERGY
    # ════════════════════════════════════════════════════════
    with tab_energy:
        st.markdown('<div class="sec-head"><span class="sec-head-title">국제 에너지 지표 시계열</span><span class="sec-head-sub">2025.02 – 2026.05 · 전쟁 발발 2026-02-28</span></div>', unsafe_allow_html=True)
        st.plotly_chart(chart_energy_timeline(energy_df), use_container_width=True)

        ec1, ec2 = st.columns([3, 2])
        with ec1:
            st.markdown('<div class="sec-head" style="margin-top:8px"><span class="sec-head-title">30일 경유가 앙상블 예측</span><span class="sec-head-sub">Prophet 40% + LSTM 60%</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_forecast(forecast_df.head(forecast_horizon)), use_container_width=True)
            st.plotly_chart(chart_shock_index(forecast_df.head(forecast_horizon)), use_container_width=True)

        with ec2:
            st.markdown('<div class="sec-head" style="margin-top:8px"><span class="sec-head-title">예측 일별 상세</span></div>', unsafe_allow_html=True)
            RC = {"LOW":"#34c77b","MEDIUM":"#e8a530","HIGH":"#f08030","CRITICAL":"#f05252"}
            for _, row in forecast_df.head(forecast_horizon).iterrows():
                rc = RC.get(row["risk_level"],"#5b6af0")
                bar_pct = int(row["shock_index"]*100)
                st.markdown(f"""
                <div class="fc-row">
                  <div class="fc-date">{row['date'].strftime('%m/%d')}</div>
                  <div>
                    <div class="fc-price">{row['ensemble']:.0f}<span style="font-size:9px;color:var(--text-3)">원</span></div>
                  </div>
                  <div class="fc-si" style="color:{rc}">SI {row['shock_index']:.3f}</div>
                  <div class="fc-bar"><div class="fc-bar-fill" style="width:{bar_pct}%;background:{rc}"></div></div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="sec-head" style="margin-top:18px"><span class="sec-head-title">위험 등급 분포</span></div>', unsafe_allow_html=True)
            rd = forecast_df.head(forecast_horizon)["risk_level"].value_counts()
            for level, color in [("CRITICAL","#f05252"),("HIGH","#f08030"),("MEDIUM","#e8a530"),("LOW","#34c77b")]:
                cnt = rd.get(level, 0); pct = cnt/forecast_horizon*100
                st.markdown(f"""
                <div class="grade-row">
                  <div class="grade-label-wrap">
                    <div class="grade-dot" style="background:{color}"></div>
                    <span class="grade-label" style="color:{color}">{level}</span>
                  </div>
                  <div class="grade-bar-track">
                    <div class="grade-bar-fill" style="width:{pct}%;background:{color}"></div>
                  </div>
                  <div class="grade-count">{cnt}일</div>
                </div>
                """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # TAB 3 · MODEL B
    # ════════════════════════════════════════════════════════
    with tab_model_b:
        m1, m2, m3, m4 = st.columns(4)
        for col, label, val, color in [
            (m1, "분석 영업소", f"{len(unit_df):,}", "var(--text-1)"),
            (m2, "Very High", f"{(unit_df['vulnerability_grade']=='Very High').sum()}", "var(--red)"),
            (m3, "HH 클러스터", f"{hh_count}", "#bc8cff"),
            (m4, "최고 취약성", f"{unit_df['vulnerability_score'].max():.4f}", "var(--amber)"),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:var(--raised);border:1px solid var(--border);border-radius:12px;
                             padding:14px 16px;text-align:center">
                  <div style="font-family:var(--mono);font-size:22px;font-weight:500;color:{color};margin-bottom:4px">{val}</div>
                  <div style="font-size:9px;color:var(--text-3);text-transform:uppercase;letter-spacing:.08em">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        bc1, bc2 = st.columns([3, 2])

        with bc1:
            st.markdown('<div class="sec-head"><span class="sec-head-title">TCS 일별 화물 교통량</span><span class="sec-head-sub">2025.01 – 2026.05</span></div>', unsafe_allow_html=True)
            war_date = pd.Timestamp("2026-02-28")
            fig_tcs = go.Figure()
            for df_p, color, name in [
                (tcs_df[tcs_df["war_period"]=="전쟁 이전"], "#5b6af0", "전쟁 이전"),
                (tcs_df[tcs_df["war_period"]=="전쟁 이후"], "#f05252", "전쟁 이후"),
            ]:
                fig_tcs.add_trace(go.Scatter(x=df_p["date"], y=df_p["freight_traffic"],
                    mode="lines", name=name, line=dict(color=color, width=1.2)))
            fig_tcs.add_vline(x=war_date, line=dict(color="#f05252", width=1, dash="dash"))
            fig_tcs.add_annotation(x=war_date, y=1, xref="x", yref="paper",
                text="전쟁 발발", showarrow=False, font=dict(color="#f05252",size=10),
                xanchor="left", xshift=5)
            dark_layout(fig_tcs, h=270)
            st.plotly_chart(fig_tcs, use_container_width=True)

            st.markdown('<div class="sec-head"><span class="sec-head-title">요일별 화물 패턴</span><span class="sec-head-sub">전쟁 전후 비교</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_tcs_war_comparison(tcs_df), use_container_width=True)

        with bc2:
            st.markdown('<div class="sec-head"><span class="sec-head-title">Vulnerability Score 분포</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_vulnerability_hist(unit_df), use_container_width=True)

            st.markdown('<div class="sec-head"><span class="sec-head-title">LISA 클러스터</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_lisa_donut(impact_df), use_container_width=True)

            st.markdown('<div class="sec-head" style="margin-top:8px"><span class="sec-head-title">구성 지표</span></div>', unsafe_allow_html=True)
            IND = [
                ("mean_freight_345_share",   "화물 비율",  "30%", "#f05252", "화물 의존 구조"),
                ("mean_freight_345_traffic", "화물 교통량","30%", "#e8a530", "규모 노출도"),
                ("traffic_volatility",       "교통 변동성","20%", "#34c77b", "충격 흡수 능력"),
                ("abs_imbalance_ratio",      "흐름 불균형","20%", "#5b6af0", "구조적 비효율"),
            ]
            for col_key, lbl, wt, color, desc in IND:
                st.markdown(f"""
                <div class="ind-card">
                  <div class="ind-ring" style="background:{color}18;border:1.5px solid {color};color:{color}">{wt}</div>
                  <div>
                    <div class="ind-title">{lbl}</div>
                    <div class="ind-desc">{desc}</div>
                    <div class="ind-code">{col_key}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        # War stats row
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        pre_m  = tcs_df[tcs_df["war_period"]=="전쟁 이전"]["freight_traffic"].mean()
        post_m = tcs_df[tcs_df["war_period"]=="전쟁 이후"]["freight_traffic"].mean()
        chg    = (post_m/pre_m-1)*100
        pre_s  = tcs_df[tcs_df["war_period"]=="전쟁 이전"]["freight_share"].mean()*100
        post_s = tcs_df[tcs_df["war_period"]=="전쟁 이후"]["freight_share"].mean()*100

        st.markdown('<div class="sec-head"><span class="sec-head-title">전쟁 전후 교통량 비교</span></div>', unsafe_allow_html=True)
        wc = st.columns(4)
        for col, lbl, val, color in [
            (wc[0], "이전 화물량 (일평균)", f"{pre_m:,.0f}대", "#5b6af0"),
            (wc[1], "이후 화물량 (일평균)", f"{post_m:,.0f}대", "#f05252"),
            (wc[2], "변화율", f"{chg:+.1f}%", "#e8a530" if chg>0 else "#34c77b"),
            (wc[3], "화물 비율 변화", f"{pre_s:.2f}% → {post_s:.2f}%", "#bc8cff"),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:var(--raised);border:1px solid var(--border);
                             border-radius:12px;padding:12px 16px">
                  <div style="font-size:9px;color:var(--text-3);text-transform:uppercase;
                               letter-spacing:.08em;margin-bottom:5px">{lbl}</div>
                  <div style="font-family:var(--mono);font-size:17px;font-weight:500;color:{color}">{val}</div>
                </div>
                """, unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # TAB 4 · INTEGRATION
    # ════════════════════════════════════════════════════════
    with tab_integration:
        st.markdown("""
        <div class="formula-banner">
          <div class="formula-label">통합 산출 공식</div>
          <div class="formula-expr">Fuel Shock Impact Score = Vulnerability Score × Diesel Shock Index</div>
          <div class="formula-note">동일한 유류 충격에서 화물 의존도가 높은 영업소의 비용 충격이 배가됩니다.</div>
        </div>
        """, unsafe_allow_html=True)

        ic1, ic2 = st.columns([3, 2])
        with ic1:
            st.markdown('<div class="sec-head"><span class="sec-head-title">취약성 vs 충격점수</span><span class="sec-head-sub">영업소 산점도</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_impact_scatter(impact_df), use_container_width=True)

            st.markdown('<div class="sec-head"><span class="sec-head-title">시나리오 비교</span><span class="sec-head-sub">기본(30일 평균) vs 최악(30일 최대)</span></div>', unsafe_allow_html=True)
            fig_sc = go.Figure()
            grade_order = ["Low","Moderate","High","Very High"]
            sc_colors   = ["#5b6af0","#e8a530","#f08030","#f05252"]
            scale = max_shock / (mean_shock + 1e-8)
            worst_score = impact_df["impact_score_mean"] * scale
            qv = worst_score.quantile([0.50,0.90,0.95])
            def wgrade(v):
                if v >= qv.iloc[2]: return "Very High"
                elif v >= qv.iloc[1]: return "High"
                elif v >= qv.iloc[0]: return "Moderate"
                return "Low"
            for grade, color in zip(grade_order, sc_colors):
                base_c  = (impact_df["impact_grade"]==grade).sum()
                worst_c = (worst_score.apply(wgrade)==grade).sum()
                fig_sc.add_trace(go.Bar(
                    name=grade, x=["기본 시나리오","최악 시나리오"],
                    y=[base_c, worst_c], marker_color=color,
                    text=[base_c, worst_c], textposition="outside",
                    textfont=dict(size=11, color="#f0f2f8"),
                ))
            fig_sc.update_layout(
                barmode="stack", plot_bgcolor="#08090c", paper_bgcolor="#08090c",
                font=dict(family="DM Sans", color="#8b91a8", size=11), height=270,
                legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.05,
                            font=dict(size=10)),
                margin=dict(l=30, r=20, t=40, b=20),
                xaxis=dict(gridcolor="#1c1e27"),
                yaxis=dict(gridcolor="#1c1e27", title="영업소 수"),
            )
            st.plotly_chart(fig_sc, use_container_width=True)

        with ic2:
            st.markdown('<div class="sec-head"><span class="sec-head-title">등급별 현황</span></div>', unsafe_allow_html=True)
            grade_def = [
                ("Very High","#f05252","badge-vh"),
                ("High",     "#e8a530","badge-hi"),
                ("Moderate", "#34c77b","badge-mod"),
                ("Low",      "#5b6af0","badge-low"),
            ]
            for grade, color, badge_cls in grade_def:
                cnt = (impact_df["impact_grade"]==grade).sum()
                pct = cnt / len(impact_df) * 100
                avg = impact_df[impact_df["impact_grade"]==grade]["impact_score_mean"].mean()
                st.markdown(f"""
                <div class="impact-card">
                  <div class="impact-card-top">
                    <span class="badge {badge_cls}">{grade}</span>
                    <div class="impact-card-num" style="color:{color}">{cnt}</div>
                  </div>
                  <div class="impact-card-meta">
                    <span>전체 중 {pct:.1f}%</span>
                    <span>평균 점수 {avg:.4f}</span>
                  </div>
                  <div class="impact-card-bar">
                    <div class="impact-card-bar-fill" style="width:{pct}%;background:{color}"></div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="sec-head" style="margin-top:18px"><span class="sec-head-title">Shock Index 요약</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            for k, v in [
                ("30일 평균", f"{mean_shock:.4f}"),
                ("30일 최대", f"{max_shock:.4f}"),
                ("최고 예측가", f"{forecast_df['ensemble'].max():.0f} 원/L"),
                ("최대 변화율", f"+{forecast_df['change_rate'].max():.2f}%"),
            ]:
                st.markdown(f'<div class="stat-row"><span class="stat-key">{k}</span><span class="stat-val">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # VH table
        st.markdown('<div class="sec-head" style="margin-top:20px"><span class="sec-head-title">Very High 등급 전체 영업소</span><span class="sec-head-sub">즉각 정책 개입 대상</span></div>', unsafe_allow_html=True)
        vh = impact_df[impact_df["impact_grade"]=="Very High"].sort_values("impact_score_mean", ascending=False)[[
            "unitName","routeName","impact_score_mean","impact_score_max",
            "vulnerability_score","vulnerability_grade","lisa_cluster",
            "mean_freight_share","traffic_volatility","abs_imbalance_ratio",
        ]].copy()
        vh["mean_freight_share"]  = (vh["mean_freight_share"]*100).round(1).astype(str)+"%"
        vh["impact_score_mean"]   = vh["impact_score_mean"].round(4)
        vh["impact_score_max"]    = vh["impact_score_max"].round(4)
        vh["vulnerability_score"] = vh["vulnerability_score"].round(4)
        vh["traffic_volatility"]  = vh["traffic_volatility"].round(3)
        vh["abs_imbalance_ratio"] = vh["abs_imbalance_ratio"].round(3)
        vh.columns = ["영업소","노선","충격(기본)","충격(최악)","취약성","취약등급","LISA","화물비율","변동성","불균형"]
        st.dataframe(vh, use_container_width=True, height=340)

    # ════════════════════════════════════════════════════════
    # TAB 5 · AI AGENT
    # ════════════════════════════════════════════════════════
    with tab_agent:
        import re
        ag1, ag2 = st.columns([3, 2])

        with ag1:
            TOOL_CHIPS = "".join(
                f'<span class="agent-tool-chip">{t}</span>'
                for t in AGENT_TOOLS
            )
            st.markdown(f"""
            <div class="agent-header">
              <div class="agent-avatar">🤖</div>
              <div style="flex:1">
                <div class="agent-name">LogisAI Agent</div>
                <div class="agent-sub">
                  <span style="display:inline-block;width:6px;height:6px;border-radius:50%;
                                background:var(--green);margin-right:5px;vertical-align:middle"></span>
                  분석 준비 완료 &nbsp;·&nbsp; ReAct 패턴 &nbsp;·&nbsp; 6 Tools
                </div>
                <div class="agent-tools-row">{TOOL_CHIPS}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # chat init
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = [{
                    "role":"agent",
                    "content":(
                        f"안녕하세요, **LogisAI**입니다.\n\n"
                        f"현재 **{len(impact_df)}개** 영업소 분석 완료 — "
                        f"Very High **{vh_count}개소**, HH 클러스터 **{hh_count}개소**, "
                        f"Shock Index 평균 **{mean_shock:.3f}**.\n\n"
                        "경유가 예측, 취약성 랭킹, LISA 분석, 전쟁 전후 비교, 시나리오 비교를 질문해 보세요."
                    ),
                    "thinking": None,
                }]

            # render chat
            chat_html = '<div class="chat-wrap">'
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    chat_html += f'<div class="msg-user">{msg["content"]}</div>'
                else:
                    think_html = ""
                    if msg.get("thinking"):
                        for stype, sdata, _ in msg["thinking"]:
                            if stype != "💬 최종 응답":
                                think_html += f'<div class="think-step"><span class="think-label">{stype}</span> → {sdata}</div>'
                    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>',
                                     msg["content"].replace("\n","<br>"))
                    chat_html += f"""
                    <div class="msg-agent">
                      <div class="msg-agent-name">LogisAI</div>
                      {think_html}
                      {content}
                    </div>"""
            chat_html += "</div>"
            st.markdown(chat_html, unsafe_allow_html=True)

            # quick questions
            st.markdown('<div class="quick-btn-label">빠른 질문</div>', unsafe_allow_html=True)
            QQ = ["경유가 예측 결과","취약성 상위 영업소","LISA 클러스터 현황",
                  "전쟁 전후 변화","시나리오 비교","노선별 위험 분석"]
            qc = st.columns(3)
            for i, q in enumerate(QQ):
                with qc[i % 3]:
                    if st.button(q, key=f"qq_{i}", use_container_width=True):
                        st.session_state["pending_query"] = q
                        st.rerun()

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            user_input = st.text_input("질문 입력",
                placeholder="예: 경유가 예측 결과 알려줘",
                key="agent_input", label_visibility="collapsed")
            sc1, sc2 = st.columns([4,1])
            with sc1:
                send_btn = st.button("전송 ↗", key="send_btn", use_container_width=True, type="primary")
            with sc2:
                if st.button("초기화", key="clr_btn", use_container_width=True):
                    st.session_state.chat_history = st.session_state.chat_history[:1]
                    st.rerun()

            # process
            query = None
            if "pending_query" in st.session_state:
                query = st.session_state.pop("pending_query")
            elif send_btn and user_input.strip():
                query = user_input.strip()
            if query:
                st.session_state.chat_history.append({"role":"user","content":query,"thinking":None})
                with st.spinner("분석 중…"):
                    time.sleep(0.6)
                    steps = agent_think(query, impact_df, forecast_df, tcs_df)
                st.session_state.chat_history.append({
                    "role":"agent","content":steps[-1][1],"thinking":steps[:-1],
                })
                st.rerun()

        with ag2:
            st.markdown('<div class="sec-head"><span class="sec-head-title">사용 가능 도구</span></div>', unsafe_allow_html=True)
            TICONS = {"경유가_예측_조회":"📈","취약성_랭킹_조회":"🏆",
                      "노선별_위험_분석":"🛣️","LISA_클러스터_조회":"🗺️",
                      "시나리오_비교":"⚖️","전쟁전후_비교":"⚔️"}
            for name, desc in AGENT_TOOLS.items():
                icon = TICONS.get(name,"🔧")
                st.markdown(f"""
                <div class="tool-card">
                  <div class="tool-card-top">
                    <span class="tool-card-icon">{icon}</span>
                    <span class="tool-card-name">{name}</span>
                  </div>
                  <div class="tool-card-desc">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown('<div class="sec-head" style="margin-top:18px"><span class="sec-head-title">분석 컨텍스트</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="card">', unsafe_allow_html=True)
            for k, v in [
                ("영업소 수", f"{len(impact_df):,}"),
                ("Very High", f"{vh_count}개소"),
                ("HH 클러스터", f"{hh_count}개소"),
                ("Shock Index", f"{mean_shock:.4f}"),
                ("최고 예측가", f"{forecast_df['ensemble'].max():.0f}원"),
                ("WTI", f"${energy_df['wti'].iloc[-1]:.2f}"),
                ("USD/KRW", f"₩{energy_df['usd_krw'].iloc[-1]:,.0f}"),
                ("VIX", f"{energy_df['vix'].iloc[-1]:.2f}"),
            ]:
                st.markdown(f'<div class="ctx-row"><span class="ctx-key">{k}</span><span class="ctx-val">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="sec-head" style="margin-top:18px"><span class="sec-head-title">추론 체계</span></div>', unsafe_allow_html=True)
            st.markdown("""
            <div class="card" style="font-size:11px;color:var(--text-3);line-height:2.2">
              <div style="color:var(--accent);font-family:var(--mono);font-size:10px;
                           margin-bottom:8px">ReAct Pattern</div>
              <div><span style="color:var(--text-1);font-weight:500">Observe</span> &nbsp;— 사용자 의도 분류</div>
              <div><span style="color:var(--text-1);font-weight:500">Think</span> &nbsp;&nbsp;&nbsp;— 최적 도구 선택</div>
              <div><span style="color:var(--text-1);font-weight:500">Act</span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— 분석 함수 실행</div>
              <div><span style="color:var(--text-1);font-weight:500">Respond</span> — 데이터 기반 답변</div>
              <div style="border-top:1px solid var(--border);margin-top:10px;padding-top:10px;color:var(--text-3)">
                확장 예정: Anthropic API · 실시간 유가 · TCS 스트림 · PostgreSQL
              </div>
            </div>
            """, unsafe_allow_html=True)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;font-size:10px;color:var(--text-3);padding:4px 0 12px;
                 letter-spacing:.04em">
      LogisRisk &nbsp;·&nbsp; Model A (Prophet + LSTM) &nbsp;·&nbsp; Model B (Vulnerability)
      &nbsp;·&nbsp; GIS: Plotly Scattergeo 2D &nbsp;·&nbsp; 한국도로공사 TCS · 오피넷 · Investing.com
    </div>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
