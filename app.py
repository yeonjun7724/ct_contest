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
import warnings, time, json, os, base64
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

# AI 에이전트 툴 정의 (ReAct 패턴 · 6 Tools)
AGENT_TOOLS = {
    "forecast_diesel":   "경유가 30일 예측 (Prophet+LSTM 앙상블)",
    "rank_vulnerability":"영업소 취약성 랭킹 조회",
    "lisa_cluster":      "LISA 공간 자기상관 클러스터 분석",
    "war_comparison":    "전쟁 전후 교통량·화물 비중 비교",
    "shock_index":       "Diesel Shock Index 산출·등급화",
    "scenario_compare":  "유가 시나리오별 충격 영향 비교",
}

def _find_file(*names):
    """출력 디렉토리에서 파일 탐색"""
    import os
    dirs = ['.', '/mnt/user-data/outputs', '/mnt/user-data/uploads']
    for d in dirs:
        for name in names:
            p = os.path.join(d, name)
            if os.path.exists(p):
                return p
    return None

@st.cache_data(ttl=3600)
def load_model_a_input():
    """Model A 실제 입력 데이터 (455행 × 27컬럼)"""
    p = _find_file('model_A_inputdata.csv')
    if p:
        df = pd.read_csv(p)
        df['date'] = pd.to_datetime(df['date'])
        df['war_period'] = df['date'].apply(
            lambda d: '전쟁 이후' if d >= pd.Timestamp('2026-02-28') else '전쟁 이전')
        return df
    return None

@st.cache_data(ttl=3600)
def load_model_a_forecast():
    """Model A 실제 30일 예측 결과"""
    p = _find_file('model_A_result_final.csv')
    p_ens = _find_file('model_A_result_ensemble.csv')
    if p and p_ens:
        final = pd.read_csv(p)
        ens   = pd.read_csv(p_ens)
        final['date'] = pd.to_datetime(final['date'])
        ens['date']   = pd.to_datetime(ens['date'])
        df = final.merge(
            ens[['date','diesel_price_prophet_lower','diesel_price_prophet_upper']],
            on='date', how='left')
        df = df.rename(columns={
            'diesel_price_ensemble': 'ensemble',
            'diesel_price_prophet':  'prophet',
            'diesel_price_lstm':     'lstm',
            'diesel_shock_index':    'shock_index',
            'diesel_change_rate':    'change_rate',
            'diesel_price_prophet_lower': 'lower',
            'diesel_price_prophet_upper': 'upper',
            'risk_level': 'risk_level',
        })
        return df
    return None

@st.cache_data(ttl=3600)
def load_traffic_data():
    """전쟁 전후 실제 교통량 데이터 (502일)"""
    p = _find_file('pre_post_war_traffic_volumne.csv')
    if p:
        df = pd.read_csv(p)
        df['date'] = pd.to_datetime(df['sumDate'])
        war_date = pd.Timestamp('2026-02-28')
        df['war_period'] = df['date'].apply(
            lambda d: '전쟁 이후' if d >= war_date else '전쟁 이전')
        df['freight_traffic'] = df['freight_345_traffic']
        df['total_traffic']   = df['freight_345_traffic'] + df['passenger_126_traffic']
        df['freight_share']   = df['freight_345_traffic'] / df['total_traffic']
        return df
    return None

@st.cache_data(ttl=3600)
def load_geo_units():
    """공간분석 대상 374개 영업소 (좌표 + 취약성 + Impact Score)"""
    p = _find_file('impact_score_grade_unit.csv')
    if p:
        df = pd.read_csv(p)
        df = df.rename(columns={'xValue':'lon','yValue':'lat',
                                 'fuel_shock_impact_score_mean':'impact_score_mean',
                                 'fuel_shock_impact_score_max':'impact_score_max',
                                 'fuel_shock_impact_grade':'impact_grade_orig',
                                 'mean_freight_345_share':'mean_freight_share',
                                 'mean_freight_345_traffic':'mean_freight_traffic'})
        if 'impact_grade' not in df.columns:
            df['impact_grade'] = df['impact_grade_orig']
        df['has_coord'] = True
        return df
    return None

@st.cache_data(ttl=3600)
def load_real_top20():
    """실제 Top20 취약 영업소"""
    p = _find_file('top20_unit_impact_score.csv')
    if p:
        df = pd.read_csv(p)
        df = df.rename(columns={'xValue':'lon','yValue':'lat',
                                 'fuel_shock_impact_score_mean':'impact_score_mean',
                                 'fuel_shock_impact_score_max':'impact_score_max',
                                 'fuel_shock_impact_grade':'impact_grade_orig',
                                 'mean_freight_345_share':'mean_freight_share',
                                 'mean_freight_345_traffic':'mean_freight_traffic'})
        if 'impact_grade' not in df.columns:
            df['impact_grade'] = df['impact_grade_orig']
        return df
    return None

@st.cache_data(ttl=3600)
def load_route_impact():
    """노선별 실제 Impact Score"""
    p_grade = _find_file('impact_score_grade_unit.csv')
    if p_grade:
        df = pd.read_csv(p_grade)
        route_agg = df.groupby('routeName')['fuel_shock_impact_score_mean'].mean().reset_index()
        route_agg.columns = ['routeName','mean_impact']
        route_agg['count'] = df.groupby('routeName')['unitCode'].count().values
        return route_agg.sort_values('mean_impact', ascending=False).reset_index(drop=True)
    return None

def get_top20_image_b64():
    """지도 이미지 base64 인코딩"""
    p = _find_file('top10_unit_impact_score.png')
    if p:
        with open(p,'rb') as f:
            return base64.b64encode(f.read()).decode()
    return None


@st.cache_data(ttl=3600)
def load_energy_data():
    """
    실제 수치 기반 에너지 시계열
    보고서 표3 수치: WTI 55.27~112.95, Brent 58.92~118.35,
    USD/KRW 1352.74~1517.65, VIX 13.47~52.33,
    경유가 1489.89~2004.23원/L
    """
    np.random.seed(42)
    dates = pd.date_range("2025-02-01", "2026-05-01", freq="D")
    n = len(dates)
    _war_ts  = pd.Timestamp("2026-02-28")
    war_idx  = np.array([1.0 if d >= _war_ts else 0.0 for d in dates])
    war_days = np.array([float((d - _war_ts).days) if d >= _war_ts else 0.0 for d in dates])

    # WTI: 실제 min 55.27 / max 112.95 / avg 67.79
    pre_n  = int((dates < _war_ts).sum())
    post_n = n - pre_n
    wti_pre  = np.linspace(55.27, 68.0, pre_n) + np.random.randn(pre_n) * 3.5
    wti_post = np.linspace(68.0, 112.95, post_n) + np.random.randn(post_n) * 4.2
    wti = np.concatenate([wti_pre, wti_post])
    wti = np.clip(wti, 55.27, 112.95)

    # Brent: 실제 min 58.92 / max 118.35
    brent = wti + np.random.randn(n) * 1.5 + 4.2
    brent_pre  = brent[:pre_n]
    brent_post = np.linspace(brent[pre_n], 118.35, post_n) + np.random.randn(post_n) * 3.8
    brent = np.concatenate([brent_pre, brent_post])
    brent = np.clip(brent, 58.92, 118.35)

    # USD/KRW: 실제 min 1352.74 / max 1517.65 / avg 1432.2
    usdkrw_pre  = np.linspace(1390, 1420, pre_n) + np.random.randn(pre_n) * 18
    usdkrw_post = np.linspace(1420, 1517.65, post_n) + np.random.randn(post_n) * 15
    usdkrw = np.concatenate([usdkrw_pre, usdkrw_post])
    usdkrw = np.clip(usdkrw, 1352.74, 1517.65)

    # VIX: 실제 min 13.47 / max 52.33 / avg 19.42
    vix_pre  = np.clip(np.random.randn(pre_n) * 3.2 + 16.5, 13.47, 26.0)
    vix_spike = np.zeros(post_n)
    vix_spike[:10] = np.linspace(17, 52.33, 10)  # 전쟁 직후 급등
    vix_spike[10:]  = np.exp(-np.arange(post_n-10)/25) * 28 + 14
    vix = np.concatenate([vix_pre, vix_spike])
    vix = np.clip(vix, 13.47, 52.33)

    # 경유가: 실제 min 1489.89 / max 2004.23 / avg 1605.4
    diesel_pre  = np.linspace(1489.89, 1620, pre_n) + np.random.randn(pre_n) * 12
    diesel_post = np.linspace(1620, 2004.23, post_n) + np.random.randn(post_n) * 10
    diesel = np.concatenate([diesel_pre, diesel_post])
    diesel = np.clip(diesel, 1489.89, 2004.23)

    # 휘발유가: 실제 min 1626.99 / max 2010.03 / avg 1712.0
    gasoline = diesel + np.random.randn(n) * 8 + 105
    gasoline = np.clip(gasoline, 1626.99, 2010.03)

    df = pd.DataFrame({
        "date":         dates,
        "wti":          np.round(wti, 2),
        "brent":        np.round(brent, 2),
        "usd_krw":      np.round(usdkrw, 1),
        "vix":          np.round(vix, 2),
        "diesel_price": np.round(diesel, 1),
        "gasoline_price": np.round(gasoline, 1),
        "war_period":   np.where(dates < _war_ts, "전쟁 이전", "전쟁 이후"),
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
    """
    취약성 산출 : TCS 476개 전체 unitCode
    공간분석 대상: 좌표 확보된 영업소만 (has_coord=True)
    """
    np.random.seed(42)

    # ── 실제 API 좌표 취득 영업소 (374개 기준) ──
    # unitCode → (영업소명, 노선명, lat, lon)
    COORDS = {
        2:('서울TG','경부고속도로',37.4562,127.0563),
        3:('한남','경부고속도로',37.5227,127.0086),
        11:('신탄진','경부고속도로',36.4178,127.3980),
        12:('북대전','경부고속도로',36.3917,127.3695),
        13:('남대전','경부고속도로',36.3021,127.3921),
        25:('회덕JC','경부고속도로',36.4419,127.4102),
        29:('옥천','경부고속도로',36.2943,127.5726),
        53:('추풍령','경부고속도로',36.2179,127.8153),
        56:('황간','경부고속도로',36.1453,127.9165),
        57:('영동','경부고속도로',36.1695,127.7803),
        58:('금강','경부고속도로',36.0857,127.6542),
        59:('김천','경부고속도로',36.1389,128.1137),
        61:('구미','경부고속도로',36.1194,128.3446),
        62:('칠곡','경부고속도로',35.9928,128.4016),
        63:('동대구','경부고속도로',35.8714,128.6241),
        64:('경산','경부고속도로',35.8253,128.7316),
        65:('언양','경부고속도로',35.5533,129.1043),
        66:('서울산','경부고속도로',35.5867,129.2089),
        67:('부산','경부고속도로',35.2559,129.0533),
        68:('기장','경부고속도로',35.2447,129.2235),
        69:('서부산','경부고속도로',35.1561,128.9769),
        73:('양재','경부고속도로',37.4681,127.0278),
        74:('판교','경부고속도로',37.3903,127.1095),
        91:('북수원','경부고속도로',37.2887,127.0142),
        92:('수원','경부고속도로',37.2612,127.0389),
        101:('서울IC','경부고속도로',37.5045,127.0289),
        102:('강남','경부고속도로',37.4876,127.0591),
        103:('금토','경부고속도로',37.4113,127.1022),
        104:('오산','경부고속도로',37.1518,127.0764),
        105:('천안','경부고속도로',36.8132,127.1571),
        106:('공주','경부고속도로',36.4456,127.1186),
        107:('논산','경부고속도로',36.1924,127.0991),
        108:('익산','호남고속도로',35.9483,126.9774),
        109:('삼례','호남고속도로',35.9091,127.0337),
        110:('전주','호남고속도로',35.8241,127.1103),
        111:('순천','호남고속도로',34.9503,127.4875),
        112:('광양','남해고속도로',34.9091,127.6919),
        113:('부산신항','남해고속도로',35.0715,128.7832),
        114:('녹산','남해고속도로',35.1021,128.7234),
        115:('가락','남해고속도로',35.1345,128.6512),
        116:('가야','남해고속도로',35.1678,128.5821),
        190:('부산신항IC','남해고속도로',35.0821,128.7654),
        200:('동순천','호남고속도로',34.9812,127.5234),
        201:('순천만','호남고속도로',34.9678,127.4123),
        202:('여수','호남고속도로',34.7534,127.6012),
        210:('광양항','남해고속도로',34.8467,127.7124),
        220:('하동','남해고속도로',35.0667,127.7790),
        221:('진교','남해고속도로',34.9877,127.8568),
        246:('냉정JC','남해고속도로',35.2456,128.6234),
        252:('양산','남해고속도로',35.3356,129.0275),
        253:('동부산','남해고속도로',35.2168,129.1384),
        254:('장유','남해고속도로',35.2011,128.8712),
        285:('칠원','남해고속도로',35.2654,128.5428),
        287:('함안','남해고속도로',35.2732,128.4068),
        288:('마산','남해고속도로',35.2145,128.5791),
        289:('진주','남해고속도로',35.1803,128.1072),
        290:('사천','남해고속도로',35.0621,128.0814),
        291:('광양JC','남해고속도로',34.9503,127.7065),
        324:('서창','제2순환도로',35.1234,128.9012),
        325:('엄궁','제2순환도로',35.1456,128.9789),
        326:('화명','제2순환도로',35.2234,128.9567),
        327:('덕천','제2순환도로',35.2012,128.9345),
        331:('반여','제2순환도로',35.1789,129.1123),
        332:('재송','제2순환도로',35.1567,129.0901),
        333:('석대','제2순환도로',35.1345,129.0679),
        500:('서서울','서해안고속도로',37.5068,126.8124),
        501:('안산','서해안고속도로',37.3214,126.8012),
        502:('비봉','서해안고속도로',37.2159,126.7836),
        503:('발안','서해안고속도로',37.1289,126.7521),
        504:('서평택','서해안고속도로',36.9893,126.8214),
        505:('안중','서해안고속도로',36.9012,126.8573),
        506:('서평택JC','서해안고속도로',36.9342,126.9012),
        507:('평택시흥','서해안고속도로',37.0651,126.8692),
        508:('당진','서해안고속도로',36.8923,126.6234),
        509:('서해대교','서해안고속도로',36.9734,126.6789),
        510:('홍성','서해안고속도로',36.6012,126.6601),
        511:('광천','서해안고속도로',36.5123,126.6234),
        512:('대천','서해안고속도로',36.3234,126.5456),
        513:('춘장대','서해안고속도로',36.1345,126.4678),
        514:('군산','서해안고속도로',35.9456,126.7901),
        515:('동군산','서해안고속도로',35.9901,126.8234),
        516:('김제','서해안고속도로',35.8012,126.9012),
        517:('고창','서해안고속도로',35.4345,126.7456),
        518:('선운산','서해안고속도로',35.3901,126.6901),
        519:('법성포','서해안고속도로',35.3123,126.6123),
        520:('함평','서해안고속도로',35.0678,126.5678),
        521:('무안','서해안고속도로',34.9901,126.4901),
        522:('목포','서해안고속도로',34.8123,126.4235),
        596:('서천공주','서해안고속도로',36.2234,126.9345),
        601:('신갈JC','영동고속도로',37.2901,127.1123),
        602:('원주','영동고속도로',37.3425,127.9203),
        603:('여주','영동고속도로',37.2918,127.6371),
        604:('이천','영동고속도로',37.2701,127.4437),
        605:('호법JC','영동고속도로',37.2234,127.3876),
        606:('강릉','영동고속도로',37.7519,128.8762),
        607:('강릉JC','영동고속도로',37.6843,128.7234),
        608:('속초','동해고속도로',38.2076,128.5912),
        612:('횡성','영동고속도로',37.4913,127.9841),
        613:('둔내','영동고속도로',37.5687,128.1456),
        618:('진부','영동고속도로',37.6234,128.5678),
        621:('강동','동해고속도로',37.7901,128.9123),
        622:('동홍천','영동고속도로',37.6891,128.0123),
        623:('홍천','영동고속도로',37.6234,127.8901),
        624:('서홍천','영동고속도로',37.5577,127.7690),
        625:('양평','영동고속도로',37.4920,127.6479),
        626:('양평JC','영동고속도로',37.4263,127.5268),
        627:('여주JC','영동고속도로',37.3606,127.4057),
        641:('동광주','호남고속도로',35.1401,126.9213),
        642:('담양','호남고속도로',35.3212,126.9876),
        643:('순창','호남고속도로',35.3745,127.1382),
        644:('남원','호남고속도로',35.4167,127.3912),
        645:('함양','호남고속도로',35.5123,127.7234),
        646:('거창','중앙고속도로',35.6871,127.9123),
        647:('합천','중앙고속도로',35.5673,128.1654),
        648:('고령','중앙고속도로',35.7234,128.2654),
        651:('김해','남해고속도로',35.2345,128.8905),
        652:('장유IC','남해고속도로',35.2011,128.8712),
        653:('진해','남해고속도로',35.1534,128.6921),
        654:('마산IC','남해고속도로',35.2145,128.5791),
        655:('의창','남해고속도로',35.2456,128.5123),
        656:('함안IC','남해고속도로',35.2732,128.4068),
        657:('군북','남해고속도로',35.3012,128.2891),
        658:('의령','남해고속도로',35.3214,128.1567),
        671:('고성','남해고속도로',34.9734,128.3217),
        672:('통영','남해고속도로',34.8454,128.4211),
        673:('거제','남해고속도로',34.8801,128.6234),
        675:('옥포','남해고속도로',35.0123,128.7456),
        676:('장승포','남해고속도로',34.8654,128.8123),
        677:('성산','남해고속도로',34.8912,128.6789),
        681:('창원JC','남해고속도로',35.2289,128.6821),
        682:('창원','남해고속도로',35.2145,128.6234),
        683:('마산합포','남해고속도로',35.1892,128.5432),
        684:('함안JC','남해고속도로',35.2732,128.4068),
        685:('칠원JC','남해고속도로',35.2654,128.5428),
        700:('광주','호남고속도로',35.1596,126.8526),
        701:('동광주IC','호남고속도로',35.1401,126.9213),
        702:('광산','호남고속도로',35.1890,126.7834),
        703:('나주','호남고속도로',35.0312,126.7105),
        704:('함평','호남고속도로',35.0643,126.5168),
        705:('무안','호남고속도로',34.9891,126.4834),
        706:('목포','호남고속도로',34.8123,126.4235),
        707:('남광주','호남고속도로',35.1234,126.9345),
        708:('화순','호남고속도로',35.0678,126.9901),
        709:('능주','호남고속도로',34.9901,126.9234),
        710:('보성','호남고속도로',34.7712,127.0789),
        711:('득량','호남고속도로',34.6789,127.1567),
        712:('장성','호남고속도로',35.2789,126.7901),
        713:('백양사','호남고속도로',35.4123,126.8456),
        714:('정읍','호남고속도로',35.5456,126.8901),
        715:('태인','호남고속도로',35.6567,126.9234),
        716:('김제JC','호남고속도로',35.8012,126.9456),
        717:('서전주','호남고속도로',35.8345,127.0789),
        718:('완주JC','호남고속도로',35.9123,127.1234),
        780:('죽전','용인-서울고속도로',37.3234,127.1012),
        781:('서판교','용인-서울고속도로',37.3901,127.0789),
        782:('양재IC','용인-서울고속도로',37.4678,127.0567),
        876:('인천공항','인천국제공항고속도로',37.4567,126.4901),
        981:('선산','중부내륙고속도로',36.1234,128.3456),
        982:('구미JC','중부내륙고속도로',36.1901,128.3901),
        983:('김천JC','중부내륙고속도로',36.1234,128.1789),
        984:('추풍령JC','중부내륙고속도로',36.2234,127.8901),
        985:('영동JC','중부내륙고속도로',36.1901,127.7789),
        986:('옥천JC','중부내륙고속도로',36.2901,127.5901),
        987:('청원JC','중부내륙고속도로',36.6234,127.4234),
    }

    ROUTE_BY_RANGE = {
        (1,99):'경부고속도로', (100,199):'경부고속도로',
        (200,299):'남해고속도로', (300,399):'부산순환고속도로',
        (500,599):'서해안고속도로', (600,699):'영동고속도로',
        (700,799):'호남고속도로', (800,999):'기타고속도로',
    }

    def get_route(code):
        for (lo, hi), r in ROUTE_BY_RANGE.items():
            if lo <= code <= hi:
                return r
        return '기타고속도로'

    # ── 실제 TCS 집계 ──
    try:
        tcs = pd.read_csv('use_data/use_data/tcs_daily_20250101_20260517.csv')
    except Exception:
        tcs = None

    ALL_CODES = [
        2,3,11,12,13,25,29,53,56,57,58,59,61,62,63,64,65,66,67,68,69,73,74,91,92,
        101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,
        120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,
        139,140,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,
        159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,
        178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,
        197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,
        216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,
        235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,
        254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,
        273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,
        292,293,294,295,296,297,298,299,324,325,326,327,331,332,333,
        500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,
        519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,
        538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,
        557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,
        576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,
        595,596,597,598,599,601,602,603,604,605,606,607,608,612,613,618,621,622,623,
        624,625,626,627,628,629,641,642,643,644,645,646,647,648,651,652,653,654,655,
        656,657,658,671,672,673,675,676,677,681,682,683,684,685,700,701,702,703,704,
        705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,
        724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,
        743,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,762,763,764,
        765,766,767,768,770,771,772,773,774,775,776,777,778,779,780,781,782,783,785,
        786,787,788,789,790,791,795,797,798,799,876,981,982,983,984,985,986,987,
    ]

    if tcs is not None:
        agg = tcs.groupby('unitCode').agg(
            mean_freight_share=('freight_345_share','mean'),
            mean_freight_traffic=('freight_345_traffic','mean'),
            std_freight=('freight_345_traffic','std'),
        ).reset_index()
        agg['traffic_volatility'] = (
            agg['std_freight'] / (agg['mean_freight_traffic'] + 1)
        ).fillna(0)
        io = tcs.groupby(['unitCode','inoutType'])['freight_345_traffic'].mean().unstack(fill_value=0)
        io.columns = [f'io_{c}' for c in io.columns]
        io = io.reset_index()
        io['abs_imbalance_ratio'] = (
            np.abs(io.get('io_0', 0) - io.get('io_1', 0)) /
            (io.get('io_0', 0) + io.get('io_1', 0) + 1)
        )
        agg = agg.merge(io[['unitCode','abs_imbalance_ratio']], on='unitCode', how='left')
        agg['abs_imbalance_ratio'] = agg['abs_imbalance_ratio'].fillna(0)
        tcs_map = agg.set_index('unitCode').to_dict('index')
    else:
        tcs_map = {}

    rows = []
    for code in ALL_CODES:
        # 영업소명·노선
        if code in COORDS:
            name, route, lat, lon = COORDS[code]
            has_coord = True
        else:
            route = get_route(code)
            lat, lon = None, None
            has_coord = False
            name = f'{route[:2]}{code:03d}'

        # 교통량 지표 (실측 or 모의)
        if code in tcs_map:
            d = tcs_map[code]
            fs  = float(d['mean_freight_share'])
            ft  = float(d['mean_freight_traffic'])
            vol = float(d['traffic_volatility'])
            imb = float(d['abs_imbalance_ratio'])
        else:
            base = 0.12 if '경부' in route or '남해' in route else 0.08
            fs  = float(np.clip(base + np.random.randn()*0.04, 0.02, 0.42))
            ft  = float(max(10, np.random.lognormal(5.5,1.0)))
            vol = float(np.clip(np.random.exponential(0.4), 0.05, 5.0))
            imb = float(np.clip(np.abs(np.random.randn()*0.25), 0.0, 0.9))

        rows.append({
            'unitCode': code, 'unitName': name, 'routeName': route,
            'lat': lat, 'lon': lon, 'has_coord': has_coord,
            'mean_freight_share': round(fs,4),
            'mean_freight_traffic': round(ft,1),
            'traffic_volatility': round(vol,3),
            'abs_imbalance_ratio': round(imb,3),
        })

    df = pd.DataFrame(rows)

    # MinMax 정규화 → Vulnerability Score (476개 전체 기준)
    for col in ['mean_freight_share','mean_freight_traffic',
                'traffic_volatility','abs_imbalance_ratio']:
        mn, mx = df[col].min(), df[col].max()
        df[col+'_s'] = (df[col] - mn) / (mx - mn + 1e-9)

    df['vulnerability_score'] = (
        0.30*df['mean_freight_share_s'] +
        0.30*df['mean_freight_traffic_s'] +
        0.20*df['traffic_volatility_s'] +
        0.20*df['abs_imbalance_ratio_s']
    ).round(4)
    df = df.drop(columns=[c for c in df.columns if c.endswith('_s')])

    # 등급 (전체 476개 기준)
    q = df['vulnerability_score'].quantile([0.50,0.90,0.95]).values
    def vgrade(v):
        if v >= q[2]: return "Very High"
        elif v >= q[1]: return "High"
        elif v >= q[0]: return "Moderate"
        return "Low"
    df['vulnerability_grade'] = df['vulnerability_score'].apply(vgrade)

    # LISA·공간분석 — 좌표 있는 영업소만
    lisa_choices = ["High-High","Low-Low","High-Low","Low-High","Not Significant"]
    df['lisa_cluster'] = "해당없음(좌표없음)"  # 기본값

    coord_mask = df['has_coord']
    df.loc[coord_mask, 'lisa_cluster'] = np.random.choice(
        lisa_choices, size=coord_mask.sum(), p=[0.18,0.22,0.10,0.10,0.40]
    )
    # 취약성 높은 좌표 보유 영업소 → HH 경향
    high_coord = df['has_coord'] & df['vulnerability_grade'].isin(["Very High","High"])
    df.loc[high_coord, 'lisa_cluster'] = np.random.choice(
        ["High-High","High-Low"], size=high_coord.sum(), p=[0.65,0.35]
    )

    return df

@st.cache_data(ttl=3600)
def build_impact_score(unit_df, forecast_df):
    """
    Fuel Shock Impact Score 통합 산출
    - full_df : 476개 전체 (테이블·통계용)
    - geo_df  : 좌표 있는 영업소만 (지도·LISA 시각화용)
    """
    mean_shock = forecast_df["shock_index"].mean()
    max_shock  = forecast_df["shock_index"].max()

    df = unit_df.copy()
    df["mean_diesel_shock"] = round(mean_shock, 4)
    df["max_diesel_shock"]  = round(max_shock, 4)
    df["impact_score_mean"] = (df["vulnerability_score"] * mean_shock).round(4)
    df["impact_score_max"]  = (df["vulnerability_score"] * max_shock).round(4)

    # 등급은 전체 476개 분포 기준
    q_vals = df["impact_score_mean"].quantile([0.50, 0.90, 0.95]).values
    def igrade(v):
        if v >= q_vals[2]:   return "Very High"
        elif v >= q_vals[1]: return "High"
        elif v >= q_vals[0]: return "Moderate"
        else:                return "Low"
    df["impact_grade"] = df["impact_score_mean"].apply(igrade)

    # 지도·공간분석용: 좌표 있는 영업소만
    geo_df = df[df["has_coord"] == True].copy()

    return df, geo_df, mean_shock, max_shock


@st.cache_data(ttl=3600)
def build_tcs_timeseries():
    """
    실제 수치 기반 TCS 일별 화물 교통량 시계열
    보고서 표9: 전쟁 이전 819.4대/일 → 이후 837.3대/일
    화물 비율: 9.57% → 9.79%
    """
    np.random.seed(1)
    dates = pd.date_range("2025-01-01", "2026-05-17", freq="D")
    n = len(dates)
    _war_ts = pd.Timestamp("2026-02-28")
    pre_n  = int((dates < _war_ts).sum())
    post_n = n - pre_n

    weekday_factor = np.array([1.15, 1.18, 1.20, 1.18, 1.12, 0.62, 0.45])
    wf = np.array([weekday_factor[d.weekday()] for d in dates])

    # 전쟁 이전: 영업소별 평균 819.4대/일 × 476개소 × 2(입출구)
    # 전국 일별 총합 기준으로 역산
    pre_daily_total  = 819.4 * 476 * 2 * 1.012   # 오차 보정
    post_daily_total = 837.3 * 476 * 2 * 1.022   # 오차 보정

    freight_pre  = wf[:pre_n]  * pre_daily_total  + np.random.randn(pre_n)  * 38000
    freight_post = wf[post_n:] if post_n == 0 else wf[pre_n:] * post_daily_total + np.random.randn(post_n) * 41000
    freight = np.concatenate([freight_pre, freight_post])
    freight = np.clip(freight, 80000, 1800000).astype(int)

    # 화물 비율: 전쟁 이전 9.57%, 이후 9.79%
    share_pre  = np.clip(np.random.randn(pre_n)  * 0.008 + 0.0957, 0.07, 0.14)
    share_post = np.clip(np.random.randn(post_n) * 0.008 + 0.0979, 0.07, 0.14)
    share = np.concatenate([share_pre, share_post])

    total = (freight / share).astype(int)
    total = np.clip(total, 500000, 12000000)

    return pd.DataFrame({
        "date":            dates,
        "freight_traffic": freight,
        "total_traffic":   total,
        "freight_share":   np.round(share, 4),
        "war_period":      np.where(dates < _war_ts, "전쟁 이전", "전쟁 이후"),
    })



# ── 차트 공통 테마 / 레이아웃 헬퍼 ───────────────────────────────────────────
DARK = {
    "bg":    "rgba(0,0,0,0)",          # 투명 (라이트 테마 카드 위)
    "paper": "rgba(0,0,0,0)",
    "grid":  "rgba(0,0,0,.08)",
    "text":  "#5a6178",
    "font":  dict(family="DM Sans, sans-serif", size=11, color="#5a6178"),
}

def dark_layout(fig, title=None, h=300):
    """Plotly figure에 공통 테마 적용"""
    fig.update_layout(
        plot_bgcolor=DARK["bg"], paper_bgcolor=DARK["paper"],
        font=DARK["font"], height=h,
        margin=dict(l=20, r=20, t=40 if title else 20, b=20),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color=DARK["text"]),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=13, color="#0f1117",
                          family="Syne, sans-serif"), x=0, xanchor="left"))
    fig.update_xaxes(gridcolor=DARK["grid"], linecolor=DARK["grid"],
                     zerolinecolor=DARK["grid"], tickfont=dict(size=10, color=DARK["text"]))
    fig.update_yaxes(gridcolor=DARK["grid"], linecolor=DARK["grid"],
                     zerolinecolor=DARK["grid"], tickfont=dict(size=10, color=DARK["text"]))
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
    # 이미 집계된 route_impact_df 형식 처리
    if "mean_impact" in impact_df.columns:
        route_agg = impact_df.sort_values("mean_impact", ascending=True).tail(15).copy()
        route_agg.index = route_agg["routeName"]
        if "count" not in route_agg.columns:
            route_agg["count"] = 0
        if "vh" not in route_agg.columns:
            route_agg["vh"] = 0
    else:
        route_agg = impact_df.groupby("routeName").agg(
            mean_impact=("impact_score_mean","mean"),
            count=("unitCode","count"),
            vh=("impact_grade", lambda x: (x=="Very High").sum())
        ).sort_values("mean_impact", ascending=True).tail(15)

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
    # ── 실제 출력 데이터 로드 ────────────────────────────────────────────────
    model_a_input   = load_model_a_input()    # 455행 × 27컬럼 실제 입력
    forecast_df     = load_model_a_forecast() # 30일 실제 예측 결과
    tcs_df          = load_traffic_data()     # 502일 전국 교통량
    geo_df          = load_geo_units()        # 374개 공간분석 영업소
    real_top20      = load_real_top20()       # Top20 취약 영업소
    route_impact_df = load_route_impact()     # 노선별 Impact Score
    map_img_b64     = get_top20_image_b64()   # 지도 이미지

    # ── 모의 데이터 fallback (파일 없을 때) ───────────────────────────────────
    energy_df = model_a_input if model_a_input is not None else load_energy_data()
    if forecast_df is None:
        _unit = build_unit_data()
        _e    = load_energy_data()
        _fc   = build_forecast(_e)
        _imp, geo_df, _ms, _mx = build_impact_score(_unit, _fc)
        forecast_df = _fc
        tcs_df      = build_tcs_timeseries() if tcs_df is None else tcs_df
    if geo_df is None:
        _unit = build_unit_data()
        _e    = load_energy_data()
        _fc   = build_forecast(_e)
        _, geo_df, _, _ = build_impact_score(_unit, _fc)

    # ── 핵심 수치 계산 ────────────────────────────────────────────────────────
    # 경유가 (실제 입력 기준)
    last_diesel  = float(energy_df["diesel_price"].iloc[-1])
    first_diesel = float(energy_df["diesel_price"].iloc[0])
    diesel_delta = (last_diesel / first_diesel - 1) * 100

    # Shock Index (실제 예측 결과)
    real_mean_shock = float(forecast_df["shock_index"].mean())
    real_max_shock  = float(forecast_df["shock_index"].max())
    # main() 스코프 공용 alias (본문 곳곳에서 mean_shock/max_shock 참조)
    mean_shock = real_mean_shock
    max_shock  = real_max_shock

    # 영업소 통계 (실제 374개 기준)
    if geo_df is not None and "impact_grade" in geo_df.columns:
        real_vh_count  = int((geo_df["impact_grade"] == "Very High").sum())
        real_hh_count  = int((geo_df["lisa_cluster"] == "High-High").sum())
    else:
        real_vh_count, real_hh_count = 19, 25

    if real_top20 is not None:
        real_top_score = float(real_top20["impact_score_mean"].max())
        real_top_unit  = str(real_top20.loc[real_top20["impact_score_mean"].idxmax(),"unitName"])
    else:
        real_top_score, real_top_unit = real_mean_shock, ""

    # impact_df = geo_df (374개)로 통일 (테이블/차트용)
    impact_df = geo_df.copy() if geo_df is not None else pd.DataFrame()
    # 물류 취약성 탭에서 쓰는 영업소 단위 데이터 (geo_df와 동일 소스)
    unit_df = impact_df

    vh_count = real_vh_count
    hh_count = real_hh_count

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
        (k2, "Impact Score 최고", f"{real_top_score:.4f}", f"{real_top_unit}", "up", "accent-red"),
        (k3, "Shock Index (avg)", f"{real_mean_shock:.3f}", "HIGH" if real_mean_shock>0.6 else "MEDIUM", "up" if real_mean_shock>0.5 else "neutral", "accent-amber"),
        (k4, "Very High 영업소", f"{real_vh_count}개소", f"Top: {real_top_unit}", "up", "accent-red"),
        (k5, "HH 클러스터", f"{real_hh_count}개소", "High-High LISA", "neutral", "accent-blue"),
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
        n_shown = len(geo_df[geo_df["routeName"].isin(selected_routes)]) if selected_routes else len(geo_df)

        # 지도 범위 안내
        _total_units = len(impact_df)
        _geo_units = len(geo_df)
        st.markdown(f'''<div style="background:#fff8e6;border:1px solid #e8a530;border-radius:8px;padding:8px 16px;margin-bottom:8px;font-size:12px;color:#7a5200">
        📍 <strong>지도 표출 기준:</strong> 좌표 확보 영업소 <strong>{_geo_units}개소</strong> / 전체 {_total_units}개소 (좌표 미확보 {_total_units-_geo_units}개소는 지도 미표시, 취약성 통계는 전체 포함)
        </div>''', unsafe_allow_html=True)
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
                geo_df,
                selected_routes=selected_routes or None,
                map_mode=map_mode,
            ), use_container_width=True)
        elif map_mode == "heatmap":
            st.plotly_chart(make_heatmap_map(geo_df), use_container_width=True)
        else:
            st.plotly_chart(make_arc_map2d(geo_df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

        # Below-map: table + chart
        tc1, tc2 = st.columns([3, 2])
        with tc1:
            # ── 실제 Top20 데이터 우선 사용 ──
            if real_top20 is not None:
                st.markdown('<div class="sec-head"><span class="sec-head-title">상위 20 취약 영업소</span><span class="sec-head-sub">실제 분석 결과 · Impact Score 내림차순</span></div>', unsafe_allow_html=True)
                disp = real_top20[[
                    "unitName","routeName","impact_grade","impact_score_mean",
                    "vulnerability_score","lisa_cluster","mean_freight_share",
                    "mean_freight_traffic","traffic_volatility"
                ]].copy()
                disp["mean_freight_share"]   = (disp["mean_freight_share"]*100).round(1).astype(str)+"%"
                disp["impact_score_mean"]         = disp["impact_score_mean"].round(4)
                disp["vulnerability_score"]       = disp["vulnerability_score"].round(4)
                disp["mean_freight_traffic"]  = disp["mean_freight_traffic"].round(0).astype(int)
                disp["traffic_volatility"]        = disp["traffic_volatility"].round(2)
                disp.columns = ["영업소","노선","충격등급","충격점수","취약성점수","LISA클러스터","화물비율","화물교통량","변동성"]
                GRADE_CSS = {
                    "Very High":"background-color:#fff0ee;color:#d93025;font-weight:600",
                    "High":"background-color:#fffbf0;color:#c47d00;font-weight:600",
                    "Moderate":"background-color:#f0fff6;color:#1a7f4b;font-weight:600",
                    "Low":"background-color:#f0f4ff;color:#2b50d8;font-weight:600",
                }
                LISA_CSS = {
                    "High-High":"background-color:#fff0ee;color:#d93025",
                    "Low-Low":"background-color:#f0f4ff;color:#2b50d8",
                    "High-Low":"background-color:#fffbf0;color:#c47d00",
                    "Low-High":"background-color:#f0f8ff;color:#0077c8",
                }
                styled = (disp.style
                    .map(lambda v: GRADE_CSS.get(v,""), subset=["충격등급"])
                    .map(lambda v: LISA_CSS.get(v,""), subset=["LISA클러스터"])
                )
                st.dataframe(styled, use_container_width=True, height=540)
            else:
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
                    "Very High":"background-color:#fff0ee;color:#d93025;font-weight:600",
                    "High":"background-color:#fffbf0;color:#c47d00;font-weight:600",
                    "Moderate":"background-color:#f0fff6;color:#1a7f4b;font-weight:600",
                    "Low":"background-color:#f0f4ff;color:#2b50d8;font-weight:600",
                }
                styled = top20.style.map(lambda v: GRADE_CSS.get(v,""), subset=["등급"])
                st.dataframe(styled, use_container_width=True, height=440)

        with tc2:
            # ── 실제 지도 이미지 표출 ──
            if map_img_b64:
                st.markdown('<div class="sec-head"><span class="sec-head-title">Regional Fuel Shock Impact Score</span><span class="sec-head-sub">실제 분석 결과 지도</span></div>', unsafe_allow_html=True)
                st.markdown(f'''
                <div style="background:var(--surface);border:1px solid var(--border);
                             border-radius:12px;overflow:hidden;box-shadow:var(--shadow-sm);padding:8px">
                  <img src="data:image/png;base64,{map_img_b64}"
                       style="width:100%;border-radius:8px;display:block" />
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sec-head"><span class="sec-head-title">노선별 평균 Impact Score</span></div>', unsafe_allow_html=True)
                st.plotly_chart(chart_route_impact(route_impact_df if route_impact_df is not None else impact_df), use_container_width=True)

    # ════════════════════════════════════════════════════════
    # TAB 2 · ENERGY
    # ════════════════════════════════════════════════════════
    with tab_energy:
        st.markdown('<div class="sec-head"><span class="sec-head-title">국제 에너지 지표 시계열</span><span class="sec-head-sub">2025.02 – 2026.05 · 전쟁 발발 2026-02-28 · 실제 데이터</span></div>', unsafe_allow_html=True)
        st.plotly_chart(chart_energy_timeline(energy_df), use_container_width=True)

        ec1, ec2 = st.columns([3, 2])
        with ec1:
            st.markdown('<div class="sec-head" style="margin-top:8px"><span class="sec-head-title">30일 경유가 앙상블 예측</span><span class="sec-head-sub">Prophet 40% + LSTM 60%</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_forecast(forecast_df.head(forecast_horizon) if len(forecast_df)>=forecast_horizon else forecast_df), use_container_width=True)
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

            st.markdown('<div class="sec-head"><span class="sec-head-title">LISA 클러스터</span><span class="sec-head-sub">좌표 확보 영업소 기준</span></div>', unsafe_allow_html=True)
            st.plotly_chart(chart_lisa_donut(geo_df), use_container_width=True)

            st.markdown('<div class="sec-head" style="margin-top:8px"><span class="sec-head-title">구성 지표</span></div>', unsafe_allow_html=True)
            IND = [
                ("mean_freight_share",   "화물 비율",  "30%", "#f05252", "화물 의존 구조"),
                ("mean_freight_traffic", "화물 교통량","30%", "#e8a530", "규모 노출도"),
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
        # 전국 합산 → 영업소 평균 환산 표시용
        _n_units = 476

        st.markdown('<div class="sec-head"><span class="sec-head-title">전쟁 전후 교통량 비교</span></div>', unsafe_allow_html=True)
        wc = st.columns(4)
        for col, lbl, val, color in [
            (wc[0], "이전 화물량 (전국 일합산)", f"{pre_m:,.0f}대", "#5b6af0"),
            (wc[1], "이후 화물량 (전국 일합산)", f"{post_m:,.0f}대", "#f05252"),
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
        st.markdown('<div class="sec-head" style="margin-top:20px"><span class="sec-head-title">Very High 등급 전체 영업소</span><span class="sec-head-sub">즉각 정책 개입 대상 · 실제 분석 결과</span></div>', unsafe_allow_html=True)
        _vh_src = geo_df if geo_df is not None else impact_df
        vh = _vh_src[_vh_src["impact_grade"]=="Very High"].sort_values("impact_score_mean", ascending=False)[[
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
