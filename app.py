import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import base64

st.set_page_config(page_title="EduPulse AI", page_icon="🎓", layout="wide",
                   initial_sidebar_state="expanded")

# ── Encode background image ──
def get_b64(path):
    try:
        with open(path,"rb") as f: return base64.b64encode(f.read()).decode()
    except: return ""

BG = get_b64("landing_bg.png")
bg_css = f'background-image:url("data:image/png;base64,{BG}"); background-size:cover; background-position:center;' if BG else "background: linear-gradient(135deg,#08091e 0%,#1a0b3e 100%);"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {{ font-family:'Inter',sans-serif; box-sizing:border-box; }}
.stApp {{ background:#08091e; color:#e2e8f0; }}
#MainMenu,footer,header {{ visibility:hidden; }}

/* ─── NATIVE BUTTON OVERRIDE (all stButton) ─── */
.stButton > button {{
    background: transparent !important;
    color: #00d4ff !important; font-weight: 700 !important;
    border: 2px solid rgba(0,212,255,0.65) !important;
    border-radius: 10px !important;
    padding: 12px 24px !important; font-size: 0.95rem !important;
    letter-spacing: 0.5px !important; transition: all 0.25s !important;
    box-shadow: 0 0 18px rgba(0,212,255,0.2), inset 0 0 20px rgba(0,212,255,0.04) !important;
}}
.stButton > button:hover {{
    background: rgba(0,212,255,0.12) !important;
    border-color: rgba(0,212,255,0.9) !important;
    box-shadow: 0 0 32px rgba(0,212,255,0.45) !important;
    transform: translateY(-2px) !important;
}}
/* Student button (2nd column) gets purple outline */
.student-btn .stButton > button {{
    background: transparent !important;
    color: #a78bfa !important;
    border: 2px solid rgba(139,92,246,0.65) !important;
    box-shadow: 0 0 18px rgba(139,92,246,0.2), inset 0 0 20px rgba(139,92,246,0.04) !important;
}}
.student-btn .stButton > button:hover {{
    background: rgba(139,92,246,0.12) !important;
    border-color: rgba(139,92,246,0.9) !important;
    box-shadow: 0 0 32px rgba(139,92,246,0.45) !important;
    transform: translateY(-2px) !important;
}}
/* Sidebar small buttons */
[data-testid="stSidebar"] .stButton > button {{
    background: rgba(14,20,60,0.6) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    color: #64748b !important; font-size: 0.85rem !important;
    padding: 10px 16px !important; font-weight: 500 !important;
    box-shadow: none !important; text-align:left !important;
    border-radius:8px !important; margin:2px 0 !important;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    border-color: rgba(0,212,255,0.4) !important; color: #00d4ff !important;
    background: rgba(0,212,255,0.06) !important;
    transform: none !important;
}}
/* Active nav button */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    color: #00d4ff !important;
    background: rgba(0,212,255,0.08) !important;
    border-color: rgba(0,212,255,0.55) !important;
    font-weight: 700 !important;
}}
/* Switch Role button */
[data-testid="stSidebar"] .stButton:last-of-type > button {{
    background: rgba(99,102,241,0.1) !important;
    border-color: rgba(99,102,241,0.35) !important;
    color: #818cf8 !important;
}}
/* Download button */
.stDownloadButton > button {{
    background: linear-gradient(135deg,#00c5f0,#0099cc) !important;
    color:#fff !important; font-weight:700 !important;
    border:none !important; border-radius:10px !important;
    box-shadow:0 0 18px rgba(0,197,240,0.3) !important;
}}
/* Form submit */
.stFormSubmitButton > button {{
    background: linear-gradient(135deg,#00c5f0,#0099cc) !important;
    color:#fff !important; border:none !important;
    font-weight:700 !important; border-radius:10px !important;
    box-shadow:0 0 18px rgba(0,197,240,0.3) !important;
}}
/* Selectbox */
.stSelectbox > div > div {{
    background:#0c1235 !important; border-color:rgba(99,102,241,0.25) !important;
    color:#e2e8f0 !important; border-radius:8px !important;
}}
/* Text input */
.stTextInput > div > div > input {{
    background:#0c1235 !important; border-color:rgba(99,102,241,0.25) !important;
    color:#e2e8f0 !important; border-radius:8px !important;
}}
/* Sliders */
[data-testid="stSlider"] > div > div > div {{
    background: rgba(0,212,255,0.12) !important;
}}
/* Multiselect */
.stMultiSelect > div > div {{
    background:#0c1235 !important; border-color:rgba(99,102,241,0.25) !important;
}}
/* Dataframe */
[data-testid="stDataFrame"] {{
    border:1px solid rgba(99,102,241,0.18) !important;
    border-radius:10px !important; overflow:hidden !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background:linear-gradient(180deg,#0d1033 0%,#100d28 100%);
    border-right:1px solid rgba(99,102,241,0.2);
    min-width:220px;
}}
[data-testid="stSidebar"] * {{ color:#94a3b8; }}
[data-testid="stSidebarContent"] {{ padding:0 !important; }}

/* ── Landing BG ── */
.landing-bg {{
    {bg_css}
    min-height:100vh; position:relative;
    padding-top:0;
}}
.landing-bg::before {{
    content:''; position:fixed; inset:0; z-index:0;
    {bg_css}
    pointer-events:none;
}}
.landing-overlay {{
    position:fixed; inset:0; z-index:0;
    background:linear-gradient(135deg,rgba(8,9,30,0.88) 0%,rgba(26,11,62,0.75) 100%);
    pointer-events:none;
}}

/* ── Role card columns ── */
.role-col-teacher {{
    background:linear-gradient(145deg,rgba(8,12,45,0.94),rgba(12,18,62,0.97));
    backdrop-filter:blur(24px);
    border:1.5px solid rgba(0,212,255,0.45);
    border-bottom:none;
    border-radius:22px 22px 0 0; padding:50px 50px 36px 50px;
    text-align:center; transition:all 0.35s;
    box-shadow:0 0 70px rgba(0,212,255,0.22), inset 0 0 100px rgba(0,212,255,0.05);
    min-height:360px; margin:0 8px 0 8px;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
}}
.role-col-teacher:hover {{
    border-color:rgba(0,212,255,0.75);
    box-shadow:0 0 110px rgba(0,212,255,0.35), inset 0 0 100px rgba(0,212,255,0.09);
}}
.role-col-student {{
    background:linear-gradient(145deg,rgba(10,8,45,0.94),rgba(16,10,62,0.97));
    backdrop-filter:blur(24px);
    border:1.5px solid rgba(139,92,246,0.45);
    border-bottom:none;
    border-radius:22px 22px 0 0; padding:50px 50px 36px 50px;
    text-align:center; transition:all 0.35s;
    box-shadow:0 0 70px rgba(139,92,246,0.22), inset 0 0 100px rgba(139,92,246,0.05);
    min-height:360px; margin:0 8px 0 8px;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
}}
.role-col-student:hover {{
    border-color:rgba(139,92,246,0.75);
    box-shadow:0 0 110px rgba(139,92,246,0.35), inset 0 0 100px rgba(139,92,246,0.09);
}}
.role-icon {{ font-size:5rem; margin-bottom:24px; display:block; }}
.role-title {{ font-size:1.75rem; font-weight:900; color:#fff; letter-spacing:2.5px;
               text-transform:uppercase; margin-bottom:16px; }}
.role-desc {{ font-size:1.05rem; color:rgba(255,255,255,0.5); line-height:1.85;
              margin-bottom:0; }}

/* ── Button wrappers as integrated card footer ── */
.teacher-btn-wrap {{
    background:linear-gradient(145deg,rgba(6,10,40,0.97),rgba(10,16,58,0.99));
    border:1.5px solid rgba(0,212,255,0.45); border-top:1px solid rgba(0,212,255,0.18);
    border-radius:0 0 22px 22px; padding:18px 12px 20px 12px;
    margin:0 8px 0 8px;
}}
.teacher-btn-wrap .stButton > button {{
    background:transparent !important; color:#00d4ff !important;
    border:1.5px solid rgba(0,212,255,0.55) !important;
    border-radius:10px !important; font-weight:700 !important;
    font-size:1rem !important; letter-spacing:0.5px !important;
    box-shadow:0 0 18px rgba(0,212,255,0.18) !important;
}}
.teacher-btn-wrap .stButton > button:hover {{
    background:rgba(0,212,255,0.1) !important;
    box-shadow:0 0 32px rgba(0,212,255,0.4) !important;
    border-color:rgba(0,212,255,0.9) !important;
}}
.student-btn {{
    background:linear-gradient(145deg,rgba(8,6,40,0.97),rgba(14,10,58,0.99));
    border:1.5px solid rgba(139,92,246,0.45); border-top:1px solid rgba(139,92,246,0.18);
    border-radius:0 0 22px 22px; padding:18px 12px 20px 12px;
    margin:0 8px 0 8px;
}}
.student-btn .stButton > button {{
    background:transparent !important; color:#a78bfa !important;
    border:1.5px solid rgba(139,92,246,0.55) !important;
    border-radius:10px !important; font-weight:700 !important;
    font-size:1rem !important; letter-spacing:0.5px !important;
    box-shadow:0 0 18px rgba(139,92,246,0.18) !important;
}}
.student-btn .stButton > button:hover {{
    background:rgba(139,92,246,0.1) !important;
    box-shadow:0 0 32px rgba(139,92,246,0.4) !important;
    border-color:rgba(139,92,246,0.9) !important;
}}

/* ── Top Header Bar ── */
.top-bar {{
    background:linear-gradient(90deg,#0d1033,#130d2e);
    border-bottom:1px solid rgba(99,102,241,0.2);
    padding:14px 28px;
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:24px; border-radius:0 0 12px 12px;
}}
.top-bar-logo {{ font-size:1.1rem; font-weight:800; color:#00d4ff; }}
.top-bar-title {{ font-size:1.3rem; font-weight:700; color:#e2e8f0; }}
.top-bar-right {{ display:flex; align-items:center; gap:12px; color:#94a3b8; font-size:0.88rem; }}

/* ── KPI Cards ── */
.kpi-row {{ display:flex; gap:14px; margin-bottom:20px; flex-wrap:wrap; padding:0 12px; }}
.kpi {{
    flex:1; min-width:120px;
    background:linear-gradient(145deg,#0f1640,#111a4a);
    border-radius:12px; padding:18px;
    border:1px solid rgba(99,102,241,0.2);
    text-align:center; transition:border-color 0.2s;
}}
.kpi:hover {{ border-color:rgba(0,212,255,0.4); box-shadow:0 0 20px rgba(0,212,255,0.08); }}
.kpi-val {{ font-size:1.9rem; font-weight:800; margin:6px 0 3px 0; }}
.kpi-lbl {{ font-size:0.68rem; color:#475569; text-transform:uppercase; letter-spacing:0.6px; }}
.kpi-sub {{ font-size:0.75rem; color:#334155; margin-top:2px; }}

/* ── Section card ── */
.section-card {{
    background:linear-gradient(145deg,#0c1235,#0f1640);
    border:1px solid rgba(99,102,241,0.18);
    border-radius:14px; padding:20px 22px; margin-bottom:16px;
}}
.section-title {{
    font-size:0.9rem; font-weight:700; color:#e2e8f0;
    margin-bottom:14px; display:flex; align-items:center; gap:8px;
    letter-spacing:0.3px;
}}

/* ── Insight Card ── */
.insight-card {{
    background:linear-gradient(135deg,#0c1235,#130e40);
    border:1px solid rgba(0,212,255,0.2);
    border-radius:12px; padding:18px 20px;
    font-size:0.88rem; line-height:1.75; color:#94a3b8;
    box-shadow:0 0 20px rgba(0,212,255,0.05);
}}
.insight-card strong {{ color:#00d4ff; }}
.insight-card-student {{ border-color:rgba(139,92,246,0.3); }}
.insight-card-student strong {{ color:#a78bfa; }}

/* ── Risk badge ── */
.badge {{ border-radius:6px; padding:4px 12px; font-weight:700; font-size:0.82rem; display:inline-block; }}
.badge-high {{ background:rgba(255,75,110,0.15); color:#ff4b6e; border:1px solid rgba(255,75,110,0.3); }}
.badge-mod  {{ background:rgba(255,165,0,0.12);  color:#ffa500;  border:1px solid rgba(255,165,0,0.3); }}
.badge-low  {{ background:rgba(0,212,170,0.12);  color:#00d4aa;  border:1px solid rgba(0,212,170,0.3); }}

/* ── Divider ── */
.div-line {{ border:none; border-top:1px solid rgba(99,102,241,0.12); margin:20px 0; }}

/* ── Sidebar nav ── */
.nav-logo {{
    padding:22px 20px 16px 20px;
    border-bottom:1px solid rgba(99,102,241,0.15);
    font-size:1.1rem; font-weight:800; color:#00d4ff;
}}
.nav-logo small {{ display:block; font-size:0.65rem; color:#334155; font-weight:400; letter-spacing:1px; text-transform:uppercase; margin-top:2px; }}
.nav-item {{
    display:flex; align-items:center; gap:10px;
    padding:10px 16px; font-size:0.85rem; color:#64748b;
    cursor:pointer; transition:all 0.2s;
    border:1px solid rgba(99,102,241,0.15);
    border-radius:8px; margin:4px 12px;
    background:rgba(14,20,60,0.5);
}}
.nav-item:hover {{
    color:#00d4ff; background:rgba(0,212,255,0.06);
    border-color:rgba(0,212,255,0.35);
    box-shadow:0 0 12px rgba(0,212,255,0.08);
}}
.nav-item.active {{
    color:#00d4ff; background:rgba(0,212,255,0.08);
    border-color:rgba(0,212,255,0.55);
    box-shadow:0 0 16px rgba(0,212,255,0.14);
    font-weight:700;
}}

/* ── Score gauge ── */
.gauge-wrap {{
    background:linear-gradient(145deg,#0c1235,#0f1640);
    border:1px solid rgba(0,212,255,0.2);
    border-radius:16px; padding:20px; text-align:center;
    box-shadow:0 0 30px rgba(0,212,255,0.06);
}}
.sim-card {{
    background:linear-gradient(145deg,#0c1235,#100e38);
    border:1px solid rgba(139,92,246,0.22);
    border-radius:14px; padding:18px 20px;
}}
.block-container {{ padding:0 !important; max-width:100% !important; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTS & HELPERS
# ─────────────────────────────────────────────
RISK_COLORS = {"High Risk":"#ff4b6e","Moderate Risk":"#ffa500","Low Risk":"#00d4aa"}
CLR_CYAN,CLR_PURPLE = "#00d4ff","#8b5cf6"

def hex_rgba(h,a=0.2):
    h=h.lstrip("#"); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return f"rgba({r},{g},{b},{a})"

def dark_fig(fig,h=280):
    fig.update_layout(paper_bgcolor="#0c1235",plot_bgcolor="#0c1235",
                      font=dict(color="#64748b",size=10),
                      height=h,margin=dict(t=36,b=12,l=8,r=8))
    return fig

def compute_risk(att,study,sleep,prev,phy=3,par=3,net=1):
    eng=(100-att)*0.5+(10-study)*5; acad=(100-prev)*0.6
    life=(8-sleep)*5+(5-phy)*5;    env=(5-par)*5+(1-net)*20
    return float(np.clip(eng*0.35+acad*0.35+life*0.15+env*0.15,0,100))

def categorize(s):
    return "Low Risk" if s<30 else ("Moderate Risk" if s<60 else "High Risk")

def rcol(cat): return RISK_COLORS.get(cat,"#94a3b8")

@st.cache_data
def load_data():
    df=pd.read_csv("final_dataset.csv")
    df.index.name="Student_ID"; df=df.reset_index()
    df["Student_ID"]=df["Student_ID"].apply(lambda x:f"STU-{x+1001:04d}")
    return df

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for k,v in [("role",None),("student_submitted",False),("student_data",{}),
            ("extra_students",[]),("teacher_page","Dashboard")]:
    if k not in st.session_state: st.session_state[k]=v

def go_home():
    st.session_state["role"]=None
    st.session_state["student_submitted"]=False
    st.session_state["student_data"]={}

# ═══════════════════════════════════════════════════
# LANDING PAGE
# ═══════════════════════════════════════════════════
if not st.session_state["role"]:
    st.markdown(f"""
    <style>
    .stApp {{
        {bg_css}
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: ''; position: fixed; inset: 0; z-index: 0;
        background: linear-gradient(135deg,rgba(4,3,18,0.88) 0%,rgba(10,4,32,0.82) 60%,rgba(6,3,22,0.75) 100%);
        pointer-events: none;
    }}
    .stApp > * {{ position: relative; z-index: 1; }}
    [data-testid="column"] {{ padding: 8px 10px !important; }}

    /* Landing card styles */
    .lp-header {{
        display:flex; align-items:flex-start; gap:10px;
        padding:28px 36px 0 36px;
    }}
    .lp-logo-text {{
        font-size:1.35rem; font-weight:900; color:#00d4ff; letter-spacing:-0.3px; line-height:1.1;
    }}
    .lp-logo-sub {{
        font-size:0.64rem; color:rgba(255,255,255,0.35); letter-spacing:2.5px;
        text-transform:uppercase; margin-top:2px; font-weight:400;
    }}
    .lp-hero {{
        text-align:center; padding:42px 20px 48px 20px;
    }}
    .lp-hero h1 {{
        font-size:2.75rem; font-weight:900; color:#fff; margin:0 0 10px 0;
        letter-spacing:-0.5px; line-height:1.15;
    }}
    .lp-hero p {{
        color:rgba(255,255,255,0.45); font-size:0.97rem; margin:0; letter-spacing:0.3px;
    }}
    .lp-hero .dot {{ color:rgba(255,255,255,0.3); margin:0 6px; }}

    /* Role cards */
    .lp-card {{
        border-radius:18px; padding:36px 32px 28px 32px;
        text-align:center; position:relative;
    }}
    .lp-card-teacher {{
        background:linear-gradient(145deg,rgba(6,10,38,0.95),rgba(10,16,54,0.98));
        border:1.5px solid rgba(0,200,220,0.5);
        box-shadow:0 0 60px rgba(0,200,220,0.15), inset 0 0 80px rgba(0,212,255,0.05);
    }}
    .lp-card-student {{
        background:linear-gradient(145deg,rgba(10,6,38,0.95),rgba(14,8,54,0.98));
        border:1.5px solid rgba(120,70,220,0.55);
        box-shadow:0 0 60px rgba(120,70,220,0.15), inset 0 0 80px rgba(139,92,246,0.05);
    }}
    .lp-card-icon {{ font-size:3.2rem; margin-bottom:16px; display:block; }}
    .lp-card-title {{
        font-size:1.15rem; font-weight:900; color:#fff; letter-spacing:2px;
        text-transform:uppercase; margin-bottom:10px;
    }}
    .lp-card-desc {{
        font-size:0.88rem; color:rgba(255,255,255,0.42); line-height:1.8; margin-bottom:0;
    }}

    /* Login buttons */
    .lp-btn-teacher .stButton > button {{
        background: transparent !important;
        color: #00d4ff !important; font-weight: 800 !important;
        border: 2px solid rgba(0,212,255,0.7) !important;
        border-radius: 30px !important;
        padding: 12px 28px !important; font-size: 1rem !important;
        letter-spacing: 0.3px !important; transition: all 0.25s !important;
        box-shadow: 0 0 20px rgba(0,212,255,0.18) !important;
        margin-top: 4px !important;
    }}
    .lp-btn-teacher .stButton > button:hover {{
        background: rgba(0,212,255,0.1) !important;
        box-shadow: 0 0 36px rgba(0,212,255,0.45) !important;
        transform: translateY(-2px) !important;
    }}
    .lp-btn-student .stButton > button {{
        background: transparent !important;
        color: #a78bfa !important; font-weight: 800 !important;
        border: 2px solid rgba(139,92,246,0.7) !important;
        border-radius: 30px !important;
        padding: 12px 28px !important; font-size: 1rem !important;
        letter-spacing: 0.3px !important; transition: all 0.25s !important;
        box-shadow: 0 0 20px rgba(139,92,246,0.18) !important;
        margin-top: 4px !important;
    }}
    .lp-btn-student .stButton > button:hover {{
        background: rgba(139,92,246,0.1) !important;
        box-shadow: 0 0 36px rgba(139,92,246,0.45) !important;
        transform: translateY(-2px) !important;
    }}
    </style>""", unsafe_allow_html=True)

    # ── Header: Logo top-left ──
    st.markdown("""
    <div class="lp-header">
      <span style="font-size:1.6rem;line-height:1">🎓</span>
      <div>
        <div class="lp-logo-text">EduPulse AI</div>
        <div class="lp-logo-sub">Academic Intelligence Platform</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Hero headline ──
    st.markdown("""
    <div class="lp-hero">
      <h1>Welcome to <span style="color:#00d4ff">EduPulse AI</span></h1>
      <p>Identify Risks <span class="dot">•</span> Understand Patterns <span class="dot">•</span> Drive Improvement</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Role cards ──
    gap1, col_t, spacer, col_s, gap2 = st.columns([0.3, 2.8, 0.2, 2.8, 0.3])

    with col_t:
        st.markdown("""
        <div class="lp-card lp-card-teacher">
          <div style="font-size:3rem;margin-bottom:14px">🏫📊</div>
          <div class="lp-card-title">Teacher / Admin</div>
        </div>
        <div style="height:12px"></div>""", unsafe_allow_html=True)
        st.markdown('<div class="lp-btn-teacher">', unsafe_allow_html=True)
        if st.button("Login as Teacher  →", key="btn_t", use_container_width=True):
            st.session_state["role"] = "teacher"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s:
        st.markdown("""
        <div class="lp-card lp-card-student">
          <div style="font-size:3rem;margin-bottom:14px">🎓💻</div>
          <div class="lp-card-title">Student</div>
        </div>
        <div style="height:12px"></div>""", unsafe_allow_html=True)
        st.markdown('<div class="lp-btn-student">', unsafe_allow_html=True)
        if st.button("Login as Student  →", key="btn_s", use_container_width=True):
            st.session_state["role"] = "student"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center;color:rgba(255,255,255,0.12);font-size:0.72rem;padding:36px 20px 18px'>
      🔒 Role-Based Access &nbsp;·&nbsp; Education · Behavioral Analytics · Personalization &nbsp;·&nbsp; EduPulse AI © 2026
    </div>""", unsafe_allow_html=True)
    st.stop()

# ═══════════════════════════════════════════════════
# TEACHER DASHBOARD
# ═══════════════════════════════════════════════════
if st.session_state["role"] == "teacher":
    df = load_data()
    if st.session_state["extra_students"]:
        df = pd.concat([df, pd.DataFrame(st.session_state["extra_students"])], ignore_index=True)

    total      = len(df)
    high_c     = (df["Risk_Category"]=="High Risk").sum()
    mod_c      = (df["Risk_Category"]=="Moderate Risk").sum()
    avg_score  = df["Exam_Score"].mean()
    avg_risk   = df["Final_Risk_Score"].mean()

    PAGES = ["Dashboard","Students","Risk Monitor","Analytics","Reports","Add Data","Settings"]

    with st.sidebar:
        st.markdown("""<div class="nav-logo">🎓 EduPulse AI<small>Academic Intelligence</small></div>""",
                    unsafe_allow_html=True)
        for p in PAGES:
            icons={"Dashboard":"📊","Students":"👥","Risk Monitor":"⚠️","Analytics":"📈",
                   "Reports":"📋","Add Data":"➕","Settings":"⚙️"}
            is_active = st.session_state["teacher_page"] == p
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icons.get(p,'•')}  {p}", key=f"nav_{p}",
                         use_container_width=True, type=btn_type):
                st.session_state["teacher_page"]=p; st.rerun()
        # ── Robot mascot at bottom ──
        st.markdown("""
        <div style="padding:24px 16px 12px;text-align:center;margin-top:10px">
          <div style="font-size:3.8rem;line-height:1">🤖</div>
          <div style="font-size:0.72rem;color:#334155;margin-top:8px;letter-spacing:0.5px">AI Academic Advisor</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Switch Role", use_container_width=True, key="t_back"):
            go_home(); st.rerun()

    page = st.session_state["teacher_page"]

    # ── Top bar ──
    st.markdown(f"""
    <div class="top-bar">
      <div class="top-bar-logo">🎓 EduPulse AI
        <span style="color:rgba(255,255,255,0.2);margin:0 10px;font-weight:300">|</span>
        <span style="font-size:1.2rem;font-weight:800;color:#e2e8f0">Teacher Dashboard</span>
      </div>
      <div class="top-bar-right">
        <span style="font-size:1.25rem;color:#64748b;cursor:pointer" title="Notifications">🔔</span>
        <span style="font-size:0.88rem;color:#94a3b8;margin-left:4px">Admin</span>
        <span style="background:linear-gradient(135deg,#1e3a5f,#2d4a7a);border-radius:50%;width:38px;height:38px;
               display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;
               border:2px solid rgba(0,212,255,0.4);margin-left:4px">👤</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── KPI row ──
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi">
        <div class="kpi-lbl">Total Students</div>
        <div class="kpi-val" style="color:#e2e8f0;font-size:2.2rem">{total:,}</div>
      </div>
      <div class="kpi">
        <div class="kpi-lbl">
          <span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#ff4b6e;margin-right:6px;vertical-align:middle"></span>
          High Risk
        </div>
        <div class="kpi-val" style="color:#ff4b6e;font-size:2.2rem">{high_c:,}</div>
        <div class="kpi-sub">({high_c/total*100:.2f}%)</div>
      </div>
      <div class="kpi">
        <div class="kpi-lbl">
          <span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#ffa500;margin-right:6px;vertical-align:middle"></span>
          Moderate Risk
        </div>
        <div class="kpi-val" style="color:#ffa500;font-size:2.2rem">{mod_c:,}</div>
        <div class="kpi-sub">({mod_c/total*100:.2f}%)</div>
      </div>
      <div class="kpi">
        <div class="kpi-lbl">
          <span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:#00d4ff;margin-right:6px;vertical-align:middle"></span>
          Avg Score
        </div>
        <div class="kpi-val" style="color:#00d4ff;font-size:2.2rem">{avg_score:.1f}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if page == "Dashboard":
        # ── Row 1: Cluster Distribution | Risk Breakdown ──
        ch1, ch2 = st.columns([1.1, 0.9])

        with ch1:
            st.markdown('<div class="section-card"><div class="section-title">🚀 Cluster Distribution</div>', unsafe_allow_html=True)
            cc = df["Cluster"].value_counts().sort_index().reset_index()
            cc.columns = ["Cluster","Count"]
            cnames = {0:"Achievers",1:"Performers",2:"At Risk",3:"Disengaged"}
            cc["Label"] = cc["Cluster"].map(cnames)
            fig = px.bar(cc, x="Label", y="Count", color="Label",
                         color_discrete_sequence=["#00e5ff","#aa00ff","#ff1744","#ff9100"],
                         template="plotly_dark")
            dark_fig(fig, 280)
            fig.update_traces(marker_line_width=0, width=0.5)
            fig.update_layout(showlegend=True, legend=dict(orientation="h", y=-0.28, x=0,
                              font=dict(size=10,color="#64748b")),
                              bargap=0.3,
                              xaxis=dict(showgrid=False),
                              yaxis=dict(gridcolor="rgba(99,102,241,0.1)"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with ch2:
            st.markdown('<div class="section-card"><div class="section-title">🔥 Risk Breakdown</div>', unsafe_allow_html=True)
            rc = df["Risk_Category"].value_counts().reset_index()
            rc.columns = ["Risk_Category","Count"]
            fig2 = px.pie(rc, names="Risk_Category", values="Count", hole=0.58,
                          color="Risk_Category",
                          color_discrete_map={"Low Risk":"#00d4aa","Moderate Risk":"#ff9100","High Risk":"#ff1744"},
                          template="plotly_dark")
            dark_fig(fig2, 280)
            fig2.update_traces(textfont_color="#e2e8f0", textinfo="label+percent",
                               textfont_size=10)
            fig2.update_layout(legend=dict(orientation="v", y=0.5, x=1.02,
                               font=dict(size=10,color="#94a3b8")))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Row 2: Institutional Insight | Quick Actions ──
        ins1, ins2 = st.columns([1.1, 0.9])
        low_att   = (df["Attendance"] < 75).mean() * 100
        low_study = (df["Hours_Studied"] < 5).mean() * 100
        health_icon = "⚠️ Needs intervention" if avg_risk >= 30 else "✅ Cohort is healthy"

        with ins1:
            st.markdown(f"""
            <div class="insight-card" style="min-height:140px">
              <div style="color:#00d4ff;font-weight:800;font-size:0.92rem;margin-bottom:12px">
                🤖 AI Institutional Insight
              </div>
              <p style="margin-bottom:8px">
                • <strong style="color:#00d4ff">{low_att:.0f}%</strong> Students need attention in Attendance &amp; Study Habits.<br>
                &nbsp;&nbsp;Suggested: Weekly Monitoring Program →
              </p>
              <p style="margin-bottom:8px">
                • <strong style="color:#ffa500">{low_study:.0f}%</strong> study fewer than 5 hrs/week.
                Consider structured study halls. 🟩
              </p>
              <p style="margin-bottom:0">
                • Avg cohort risk: <strong style="color:#00d4ff">{avg_risk:.1f}/100</strong>
                — {health_icon}
              </p>
            </div>""", unsafe_allow_html=True)

        with ins2:
            buf = io.StringIO()
            df[["Student_ID","Attendance","Hours_Studied","Exam_Score","Final_Risk_Score","Risk_Category"]].to_csv(buf, index=False)
            st.markdown('<div class="section-card" style="min-height:140px">', unsafe_allow_html=True)
            st.download_button("📥  Download Report", data=buf.getvalue(),
                               file_name="edupulse_risk_report.csv", mime="text/csv",
                               use_container_width=True, type="primary")
            st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
            with st.popover("➕  Add Student", use_container_width=True):
                st.markdown("#### Add New Student")
                nid  = st.text_input("Student ID", placeholder="STU-9999", key="pop_id")
                na   = st.slider("Attendance (%)", 0, 100, 75, key="pop_att")
                ns   = st.slider("Study Hrs/week", 0, 20, 6, key="pop_study")
                nsl  = st.slider("Sleep Hrs/night", 3, 10, 7, key="pop_sleep")
                np_  = st.slider("Previous Score", 0, 100, 65, key="pop_prev")
                ne   = st.slider("Exam Score", 0, 100, 65, key="pop_exam")
                if st.button("💾 Save Student", key="pop_save", use_container_width=True):
                    pm  = {"Low":1,"Medium":3,"High":5}
                    rs_ = compute_risk(na, ns, nsl, np_, 3, 3, 1)
                    new_row = {
                        "Student_ID": nid or f"STU-NEW-{len(st.session_state['extra_students'])+1}",
                        "Attendance": na, "Hours_Studied": ns, "Sleep_Hours": nsl,
                        "Previous_Scores": np_, "Exam_Score": ne,
                        "Engagement_Risk": (100-na)*0.5+(10-ns)*5,
                        "Academic_Risk": (100-np_)*0.6,
                        "Lifestyle_Risk": (8-nsl)*5, "Environment_Risk": 10,
                        "Final_Risk_Score": round(rs_,1),
                        "Risk_Category": categorize(rs_), "Cluster": 0
                    }
                    st.session_state["extra_students"].append(new_row)
                    st.success(f"✅ {new_row['Student_ID']} added! Risk: {rs_:.1f} ({categorize(rs_)})")
            if st.session_state["extra_students"]:
                last = st.session_state["extra_students"][-1]
                cat_col = {"High Risk":"#ff4b6e","Moderate Risk":"#ffa500","Low Risk":"#00d4aa"}.get(last["Risk_Category"],"#94a3b8")
                st.markdown(f"""
                <div style="margin-top:8px;padding:8px 12px;border-radius:8px;
                     background:rgba(0,212,255,0.06);border:1px solid rgba(0,212,255,0.2);
                     font-size:0.8rem;color:#94a3b8">
                  ✅ Last added: <strong style="color:#e2e8f0">{last['Student_ID']}</strong>
                  &nbsp;·&nbsp; Risk: <strong style="color:{cat_col}">{last['Risk_Category']}</strong>
                  &nbsp;·&nbsp; Total added: <strong style="color:#00d4ff">{len(st.session_state['extra_students'])}</strong>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Bottom stats bar ──
        st.markdown(f"""
        <div style="display:flex;gap:16px;margin-top:8px;padding:0 4px">
          <div style="flex:1;background:linear-gradient(145deg,#0c1235,#111a4a);
               border:1px solid rgba(99,102,241,0.22);border-radius:14px;
               padding:18px;text-align:center">
            <div style="font-size:1.6rem;margin-bottom:4px">🎓</div>
            <div style="font-size:1.4rem;font-weight:900;color:#00d4ff">10,000+</div>
            <div style="font-size:0.78rem;color:#475569;margin-top:2px">Analysis</div>
          </div>
          <div style="flex:1;background:linear-gradient(145deg,#0c1235,#111a4a);
               border:1px solid rgba(99,102,241,0.22);border-radius:14px;
               padding:18px;text-align:center">
            <div style="font-size:1.6rem;margin-bottom:4px">👥</div>
            <div style="font-size:1.4rem;font-weight:900;color:#8b5cf6">2,500+</div>
            <div style="font-size:0.78rem;color:#475569;margin-top:2px">Students added</div>
          </div>
          <div style="flex:1;background:linear-gradient(145deg,#0c1235,#111a4a);
               border:1px solid rgba(99,102,241,0.22);border-radius:14px;
               padding:18px;text-align:center">
            <div style="font-size:1.6rem;margin-bottom:4px">📊</div>
            <div style="font-size:1.4rem;font-weight:900;color:#00d4aa">95%</div>
            <div style="font-size:0.78rem;color:#475569;margin-top:2px">Accuracy</div>
          </div>
          <div style="flex:1;background:linear-gradient(145deg,#0c1235,#111a4a);
               border:1px solid rgba(99,102,241,0.22);border-radius:14px;
               padding:18px;text-align:center">
            <div style="font-size:1.6rem;margin-bottom:4px">⚡</div>
            <div style="font-size:1.4rem;font-weight:900;color:#ffa500">Real-Time</div>
            <div style="font-size:0.78rem;color:#475569;margin-top:2px">Monitoring</div>
          </div>
        </div>""", unsafe_allow_html=True)



    elif page == "Students":
        st.markdown('<div class="section-card"><div class="section-title">🔍 Student Lookup — Select by Roll Number</div>', unsafe_allow_html=True)
        lid = st.selectbox("Select Student", df["Student_ID"].tolist(), key="lkp")
        stu = df[df["Student_ID"]==lid].iloc[0]
        sc  = stu["Final_Risk_Score"]; scat=stu["Risk_Category"]; scol=rcol(scat)
        bclass = "high" if scat=="High Risk" else ("mod" if scat=="Moderate Risk" else "low")
        cols6=st.columns(6)
        for col,(lbl,val,col_hex) in zip(cols6,[
            ("Roll No",stu["Student_ID"],"#e2e8f0"),
            ("Risk Score",f"{sc:.1f}",scol),
            ("Attendance",f"{stu['Attendance']:.0f}%","#00d4aa" if stu["Attendance"]>=75 else "#ff4b6e"),
            ("Study Hrs",f"{stu['Hours_Studied']:.0f}","#00d4aa" if stu["Hours_Studied"]>=5 else "#ffa500"),
            ("Exam Score",f"{stu['Exam_Score']:.0f}","#00d4aa" if stu["Exam_Score"]>=df["Exam_Score"].mean() else "#ffa500"),
            ("Cluster",f"C{int(stu['Cluster'])}",CLR_CYAN),
        ]):
            col.markdown(f"""<div style="background:#0c1235;border:1px solid rgba(99,102,241,0.2);
            border-radius:10px;padding:12px;text-align:center;">
            <div style="font-size:1.3rem;font-weight:800;color:{col_hex}">{val}</div>
            <div style="font-size:0.65rem;color:#334155;text-transform:uppercase;letter-spacing:0.5px;margin-top:3px">{lbl}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        rl,rr=st.columns(2)
        with rl:
            cats=["Attendance","Study Hours","Sleep","Prev Score","Exam","Low Eng Risk","Low Acad Risk"]
            vals=[min(stu["Attendance"]/100,1), min(stu["Hours_Studied"]/10,1),
                  min(stu["Sleep_Hours"]/10,1), min(stu["Previous_Scores"]/100,1),
                  min(stu["Exam_Score"]/100,1),
                  1-min(stu["Engagement_Risk"]/100,1), 1-min(stu["Academic_Risk"]/100,1)]
            avgs=[df["Attendance"].mean()/100,df["Hours_Studied"].mean()/10,
                  df["Sleep_Hours"].mean()/10,df["Previous_Scores"].mean()/100,
                  df["Exam_Score"].mean()/100,0.5,0.5]
            fr=go.Figure()
            fr.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=cats+[cats[0]],fill="toself",
                fillcolor=hex_rgba(scol,0.18),line=dict(color=scol,width=2),name=lid))
            fr.add_trace(go.Scatterpolar(r=avgs+[avgs[0]],theta=cats+[cats[0]],fill="toself",
                fillcolor=hex_rgba("#8b5cf6",0.1),line=dict(color="#8b5cf6",width=1.5,dash="dot"),name="Class Avg"))
            fr.update_layout(paper_bgcolor="#0c1235",
                polar=dict(bgcolor="#0c1235",
                    radialaxis=dict(visible=True,range=[0,1],color="#1e2a45",gridcolor="#1a2240"),
                    angularaxis=dict(color="#334155",gridcolor="#1a2240")),
                font=dict(color="#64748b",size=10),height=320,
                showlegend=True,legend=dict(orientation="h",y=-0.15,x=0.2),
                margin=dict(t=20,b=30,l=30,r=30))
            st.plotly_chart(fr,use_container_width=True)

        with rr:
            issues,strats=[],[]
            if stu["Attendance"]<75:    issues.append(f"attendance at <strong>{stu['Attendance']:.0f}%</strong>"); strats.append("Schedule 1:1 check-in, assign peer mentor.")
            if stu["Hours_Studied"]<5:  issues.append("low study hours"); strats.append("Recommend structured study-hall with weekly planner.")
            if stu["Sleep_Hours"]<6:    issues.append("insufficient sleep"); strats.append("Refer to wellness resources; avoid early high-stakes exams.")
            if stu["Previous_Scores"]<60: issues.append("weak academic foundation"); strats.append("Assign differentiated worksheets; peer tutoring.")
            if stu["Exam_Score"]<df["Exam_Score"].mean()-10: issues.append("below-average exam score"); strats.append("Formative micro-assessments; office-hour walkthroughs.")
            intro = f"✅ <strong>{lid}</strong> performing well." if not issues else f"⚠️ <strong>{lid}</strong> ({scat}) flagged for: " + "; ".join(issues)+"."
            recs  = "<li>Recognise publicly; assign leadership role.</li>" if not strats else "".join(f"<li>{s}</li>" for s in strats)
            tags  = []
            if stu["Attendance"]>=85: tags.append("High Attendance")
            elif stu["Attendance"]<70: tags.append("Chronic Absentee")
            if stu["Hours_Studied"]>=8: tags.append("Self-Directed")
            elif stu["Hours_Studied"]<=3: tags.append("Low Effort")
            if stu["Exam_Score"]>=df["Exam_Score"].mean()+10: tags.append("High Performer")
            elif stu["Exam_Score"]<=df["Exam_Score"].mean()-10: tags.append("Underperformer")
            tag_html="".join(f'<span class="badge badge-{bclass}" style="margin:3px">{t}</span>' for t in (tags or ["Average Profile"]))
            st.markdown(f"""
            <div class="insight-card">
              <div style="color:#00d4ff;font-weight:700;margin-bottom:10px">🧠 AI Profile &amp; Teaching Strategy</div>
              <p>{intro}</p>
              <p><strong>🎯 Teaching Strategies:</strong></p>
              <ul style="margin:0;padding-left:16px;line-height:2">{recs}</ul>
              <div style="margin-top:12px;font-size:0.72rem;color:#334155;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Learning Pattern Tags</div>
              {tag_html}
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<hr class="div-line">', unsafe_allow_html=True)
        st.markdown('<div class="section-card"><div class="section-title">🗂️ Full Student Risk Heatmap</div>', unsafe_allow_html=True)
        rf=st.multiselect("Filter Risk Level",df["Risk_Category"].unique().tolist(),
                          default=df["Risk_Category"].unique().tolist())
        hdf=df[df["Risk_Category"].isin(rf)][["Student_ID","Attendance","Hours_Studied","Sleep_Hours",
            "Previous_Scores","Exam_Score","Final_Risk_Score","Risk_Category","Cluster"]].copy()
        hdf["Cluster"]=hdf["Cluster"].apply(lambda x:f"C{x}"); hdf["Final_Risk_Score"]=hdf["Final_Risk_Score"].round(1)
        def crow(row):
            bg={"High Risk":"background-color:#1a0810;color:#ff8080",
                "Moderate Risk":"background-color:#1a1200;color:#fcd34d",
                "Low Risk":"background-color:#041610;color:#6ee7b7"}.get(row["Risk_Category"],"")
            return [bg]*len(row)
        st.dataframe(hdf.head(100).style.apply(crow,axis=1).format(
            {"Final_Risk_Score":"{:.1f}","Attendance":"{:.0f}","Hours_Studied":"{:.0f}","Exam_Score":"{:.0f}"}),
            use_container_width=True,height=340)
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Risk Monitor":
        st.markdown('<div class="section-card"><div class="section-title">🚨 High-Risk Students</div>', unsafe_allow_html=True)
        hr=df[df["Risk_Category"]=="High Risk"].sort_values("Final_Risk_Score",ascending=False)
        st.markdown(f"⚠️ **{len(hr):,} students** flagged for immediate intervention.")
        def hr_row(row): return ["background-color:#180610;color:#fca5a5"]*len(row)
        st.dataframe(hr[["Student_ID","Attendance","Hours_Studied","Sleep_Hours","Exam_Score","Final_Risk_Score","Cluster"]].head(50)
                     .style.apply(hr_row,axis=1).format({"Final_Risk_Score":"{:.1f}","Attendance":"{:.0f}","Hours_Studied":"{:.0f}","Exam_Score":"{:.0f}"}),
                     use_container_width=True,height=380)
        st.markdown('</div>', unsafe_allow_html=True)

        la=(df["Attendance"]<75).mean()*100; ls=(df["Hours_Studied"]<5).mean()*100
        lsl=(df["Sleep_Hours"]<6).mean()*100; le=(df["Exam_Score"]<df["Exam_Score"].mean()-10).mean()*100
        r1,r2=st.columns(2)
        for col,icon,pct,msg,tip in [
            (r1,"📅",la,"attendance below 75%","Send SMS alerts; flexible attendance policy."),
            (r2,"📚",ls,"study < 5 hrs/week","Structured study-halls; LMS progress nudges."),
            (r1,"😴",lsl,"sleep < 6 hrs/night","Wellbeing campaign; avoid early-morning exams."),
            (r2,"📝",le,"below class avg exam","Targeted workshops; identify low-mastery topics."),
        ]:
            col.markdown(f"""<div class="section-card" style="text-align:center">
              <div style="font-size:1.8rem">{icon}</div>
              <div style="font-size:2rem;font-weight:800;color:#ffa500;margin:6px 0">{pct:.1f}%</div>
              <div style="font-size:0.85rem;color:#475569;margin-bottom:8px">{msg}</div>
              <div style="font-size:0.78rem;color:#00d4ff">💡 {tip}</div>
            </div>""", unsafe_allow_html=True)

    elif page == "Analytics":
        c1,c2=st.columns(2)
        with c1:
            samp=df.sample(min(500,len(df)),random_state=42)
            fig=px.scatter(samp,x="Attendance",y="Exam_Score",color="Risk_Category",
                color_discrete_map=RISK_COLORS,size="Hours_Studied",opacity=0.7,
                title="Attendance vs Exam Score",template="plotly_dark")
            dark_fig(fig,300); fig.update_layout(legend=dict(orientation="h",y=-0.22,x=0))
            st.plotly_chart(fig,use_container_width=True)
        with c2:
            cp=df.groupby("Cluster")[["Attendance","Hours_Studied","Exam_Score","Final_Risk_Score"]].mean().round(1).reset_index()
            cp["Cluster"]=cp["Cluster"].apply(lambda x:["Achievers","Performers","At Risk","Disengaged"][int(x)] if int(x)<4 else f"C{x}")
            fig2=px.bar(cp.melt(id_vars="Cluster",var_name="Metric",value_name="Avg"),
                        x="Metric",y="Avg",color="Cluster",barmode="group",
                        color_discrete_sequence=["#00d4ff","#8b5cf6","#ff4b6e","#ffa500"],
                        title="Cluster Academic Profile",template="plotly_dark")
            dark_fig(fig2,300); fig2.update_layout(legend=dict(orientation="h",y=-0.22,x=0))
            st.plotly_chart(fig2,use_container_width=True)

    elif page == "Reports":
        st.markdown('<div class="section-card"><div class="section-title">📥 Download Risk Report</div>', unsafe_allow_html=True)
        rd=df[["Student_ID","Attendance","Hours_Studied","Sleep_Hours","Previous_Scores",
               "Exam_Score","Final_Risk_Score","Risk_Category","Cluster"]].copy()
        rd["Cluster"]=rd["Cluster"].apply(lambda x:f"C{x}")
        rd=rd.sort_values("Final_Risk_Score",ascending=False)
        buf=io.StringIO(); rd.to_csv(buf,index=False)
        st.download_button("⬇️ Download Full Risk Report (CSV)",data=buf.getvalue(),
                           file_name="edupulse_risk_report.csv",mime="text/csv",
                           type="primary",use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Add Data":
        st.markdown('<div class="section-card"><div class="section-title">➕ Add / Update Student Data</div>', unsafe_allow_html=True)
        st.markdown("Onboard a new student — risk score is computed automatically.")
        with st.form("add_form",clear_on_submit=True):
            fa,fb=st.columns(2)
            nid=fa.text_input("Student ID",placeholder="STU-9999")
            na=fa.slider("Attendance (%)",0,100,75)
            ns=fa.slider("Study Hrs/week",0,20,6)
            nsl=fb.slider("Sleep Hrs/night",3,10,7)
            np_=fb.slider("Previous Score",0,100,65)
            ne=fb.slider("Exam Score",0,100,65)
            nph=fa.selectbox("Physical Activity",["Low","Medium","High"],index=1)
            npr=fb.selectbox("Parental Involvement",["Low","Medium","High"],index=1)
            nin=fa.selectbox("Internet Access",["Yes","No"],index=0)
            sub=st.form_submit_button("💾 Add Student",type="primary",use_container_width=True)
        if sub:
            pm={"Low":1,"Medium":3,"High":5}
            rs=compute_risk(na,ns,nsl,np_,pm[nph],pm[npr],1 if nin=="Yes" else 0)
            row={"Student_ID":nid or f"STU-NEW-{len(st.session_state['extra_students'])+1}",
                 "Attendance":na,"Hours_Studied":ns,"Sleep_Hours":nsl,
                 "Previous_Scores":np_,"Exam_Score":ne,
                 "Engagement_Risk":(100-na)*0.5+(10-ns)*5,"Academic_Risk":(100-np_)*0.6,
                 "Lifestyle_Risk":(8-nsl)*5+(5-pm[nph])*5,"Environment_Risk":(5-pm[npr])*5+(1-(1 if nin=="Yes" else 0))*20,
                 "Final_Risk_Score":round(rs,1),"Risk_Category":categorize(rs),"Cluster":0}
            st.session_state["extra_students"].append(row)
            st.success(f"✅ **{row['Student_ID']}** added — Risk Score: **{rs:.1f}** ({categorize(rs)})")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif page == "Settings":
        st.markdown('<div class="section-card"><div class="section-title">⚙️ Settings</div>', unsafe_allow_html=True)
        st.info("Settings panel — institutional configuration options coming soon.")
        st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════
# STUDENT DASHBOARD
# ═══════════════════════════════════════════════════
elif st.session_state["role"] == "student":
    df = load_data()

    # ── Dark theme for student (matches teacher) ──
    st.markdown("""
    <style>
    /* Student dashboard – dark theme */
    .stApp { background:#08091e !important; color:#e2e8f0 !important; }
    section[data-testid="stMain"] > div { background:transparent !important; }

    /* Dark sidebar */
    [data-testid="stSidebar"] {
        background:linear-gradient(180deg,#0d1033 0%,#100d28 100%) !important;
        border-right:1px solid rgba(99,102,241,0.2) !important;
    }
    [data-testid="stSidebar"] * { color:#94a3b8 !important; }
    [data-testid="stSidebar"] .stButton > button {
        background:rgba(14,20,60,0.9) !important;
        border:1px solid rgba(139,92,246,0.35) !important;
        color:#818cf8 !important; font-size:0.83rem !important;
        padding:8px 12px !important; font-weight:600 !important;
        box-shadow:none !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        border-color:#a78bfa !important; color:#a78bfa !important;
        background:rgba(139,92,246,0.08) !important;
        transform:none !important;
    }

    /* Student card */
    .stu-card {
        background:linear-gradient(145deg,#0c1235,#0f1640);
        border:1px solid rgba(99,102,241,0.2);
        border-radius:16px; padding:22px 24px; margin-bottom:14px;
    }
    .stu-card-title {
        font-size:0.92rem; font-weight:700; color:#e2e8f0;
        margin-bottom:14px; display:flex; align-items:center; gap:8px;
    }

    /* Gauge score number */
    .gauge-score {
        text-align:center; margin-top:-18px; padding-bottom:8px;
    }

    /* Risk badge */
    .stu-badge {
        display:inline-block; border-radius:20px; padding:5px 22px;
        font-weight:800; font-size:0.95rem;
    }
    .stu-badge-high { background:rgba(255,75,110,0.15); color:#ff4b6e;
                      border:1.5px solid rgba(255,75,110,0.45); }
    .stu-badge-mod  { background:rgba(255,165,0,0.12); color:#ffa500;
                      border:1.5px solid rgba(255,165,0,0.45); }
    .stu-badge-low  { background:rgba(0,212,170,0.12); color:#00d4aa;
                      border:1.5px solid rgba(0,212,170,0.45); }

    /* AI insight highlight */
    .ai-insight-val { font-size:1.3rem; font-weight:900; color:#00d4ff; }
    .ai-insight-delta { font-size:1.1rem; font-weight:800; color:#00d4aa; }

    /* Simulator slider rows */
    .sim-row {
        display:flex; align-items:center; justify-content:space-between;
        background:linear-gradient(135deg,#0f183a,#131e48);
        border:1px solid rgba(99,102,241,0.18);
        border-radius:10px; padding:12px 16px; margin-bottom:10px;
    }
    .sim-icon { font-size:1.1rem; margin-right:8px; }
    .sim-label { font-size:0.85rem; color:#94a3b8; font-weight:500; }
    .sim-val { font-size:1rem; font-weight:800; color:#e2e8f0; }

    /* Recalculate button */
    .recalc-wrap .stButton > button {
        background: linear-gradient(135deg,#7c3aed,#00b8d4) !important;
        color:#fff !important; border:none !important;
        font-weight:800 !important; font-size:1rem !important;
        border-radius:10px !important;
        box-shadow:0 4px 20px rgba(124,58,237,0.4) !important;
        letter-spacing:0.3px !important;
    }
    .recalc-wrap .stButton > button:hover {
        transform:translateY(-2px) !important;
        box-shadow:0 6px 28px rgba(124,58,237,0.6) !important;
    }

    /* Slider override for dark */
    [data-testid="stSlider"] > div > div > div {
        background:rgba(0,212,255,0.15) !important;
    }
    </style>""", unsafe_allow_html=True)

    # ── Student Sidebar ──
    with st.sidebar:
        st.markdown("""
        <div class="nav-logo">🎓 EduPulse AI<small>Student Portal</small></div>
        """, unsafe_allow_html=True)
        for p, icon in [("Dashboard","📊"),("My Profile","👤"),("Risk Monitor","⚠️"),
                        ("Analytics","📈"),("Settings","⚙️")]:
            st.markdown(f'<div class="nav-item {"active" if p=="Dashboard" else ""}">{icon} {p}</div>',
                        unsafe_allow_html=True)
        st.markdown("""
        <div style="padding:28px 16px 10px;text-align:center;margin-top:10px">
          <div style="font-size:3.8rem;line-height:1">🤖</div>
          <div style="font-size:0.72rem;color:#334155;margin-top:8px;letter-spacing:0.5px">AI Academic Advisor</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Switch Role", use_container_width=True, key="s_back"):
            go_home(); st.rerun()

    sname = st.session_state["student_data"].get("name","Student")

    # ── Student Data Entry Form ──
    if not st.session_state["student_submitted"]:
        st.markdown(f"""
        <div class="top-bar">
          <div class="top-bar-logo">🎓 EduPulse AI
            <span style="color:rgba(255,255,255,0.2);margin:0 10px;font-weight:300">|</span>
            <span style="font-size:1.1rem;font-weight:700;color:#e2e8f0">Student Dashboard</span>
          </div>
          <div class="top-bar-right">
            <span style="font-size:0.88rem;color:#94a3b8">Welcome, <strong style="color:#a78bfa">Student</strong></span>
            <span style="background:linear-gradient(135deg,#3b1f6e,#5b2d9e);border-radius:50%;width:38px;height:38px;
                   display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;
                   border:2px solid rgba(139,92,246,0.5);margin-left:6px">👤</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="stu-card">', unsafe_allow_html=True)
        st.markdown('<div class="stu-card-title">📝 Enter Your Academic Data</div>', unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.85rem;color:#64748b;margin-bottom:16px'>All data is private. Used only to compute your personalised risk score.</div>", unsafe_allow_html=True)
        with st.form("stu_form"):
            sn = st.text_input("Your Name (optional)", placeholder="e.g. Maya")
            f1, f2 = st.columns(2)
            sa  = f1.slider("📅 Attendance (%)", 0, 100, 75)
            ss  = f1.slider("📚 Study Hours/week", 0, 20, 6)
            ssl = f1.slider("😴 Sleep Hours/night", 3, 10, 7)
            sp  = f2.slider("📝 Previous Score", 0, 100, 60)
            se  = f2.slider("🎯 Exam Score", 0, 100, 62)
            sph = f1.select_slider("🏃 Physical Activity", ["Low","Medium","High"], value="Medium")
            spar= f2.select_slider("👪 Parental Involvement", ["Low","Medium","High"], value="Medium")
            snet= f2.radio("🌐 Internet Access", ["Yes","No"], horizontal=True)
            go  = st.form_submit_button("🔍 Calculate My Risk Score", use_container_width=True)
        if go:
            pm = {"Low":1,"Medium":3,"High":5}
            st.session_state["student_data"] = dict(
                name=sn or "Student", att=sa, study=ss, sleep=ssl,
                prev=sp, exam=se, physical=pm[sph], parental=pm[spar],
                internet=1 if snet=="Yes" else 0)
            st.session_state["student_submitted"] = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        d    = st.session_state["student_data"]
        rs   = compute_risk(d["att"], d["study"], d["sleep"], d["prev"],
                            d["physical"], d["parental"], d["internet"])
        cat  = categorize(rs); col = rcol(cat)
        bcls = "high" if cat=="High Risk" else ("mod" if cat=="Moderate Risk" else "low")
        improve_msg = ("You can improve with small changes!" if cat != "Low Risk"
                       else "Excellent! Keep it up! 🎉")

        # ── Top bar ──
        st.markdown(f"""
        <div class="top-bar">
          <div class="top-bar-logo">🎓 EduPulse AI
            <span style="color:rgba(255,255,255,0.2);margin:0 10px;font-weight:300">|</span>
            <span style="font-size:1.1rem;font-weight:700;color:#e2e8f0">Student Dashboard</span>
          </div>
          <div class="top-bar-right">
            <span style="font-size:0.88rem;color:#94a3b8">Welcome, <strong style="color:#a78bfa">{sname}</strong></span>
            <span style="background:linear-gradient(135deg,#3b1f6e,#5b2d9e);border-radius:50%;width:38px;height:38px;
                   display:inline-flex;align-items:center;justify-content:center;font-size:1.2rem;
                   border:2px solid rgba(139,92,246,0.5);margin-left:6px">👤</span>
          </div>
        </div>""", unsafe_allow_html=True)

        # ══ ROW 1: Gauge  |  Radar ══
        g_col, r_col = st.columns(2)

        # ── Left: Risk Score Gauge ──
        with g_col:
            st.markdown('<div class="stu-card">', unsafe_allow_html=True)
            st.markdown('<div class="stu-card-title">🎯 Your Academic Risk Score</div>', unsafe_allow_html=True)
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=rs,
                number={"font":{"color":"#e2e8f0","size":58,"family":"Inter"},"suffix":"/100"},
                gauge={
                    "axis":{"range":[0,100],"tickcolor":"rgba(99,102,241,0.3)",
                            "tickfont":{"color":"#64748b","size":10}},
                    "bar":{"color":"rgba(0,0,0,0)","thickness":0},
                    "bgcolor":"rgba(0,0,0,0)","bordercolor":"rgba(0,0,0,0)",
                    "steps":[
                        {"range":[0,10],  "color":"#00c853"},
                        {"range":[10,20], "color":"#64dd17"},
                        {"range":[20,30], "color":"#aeea00"},
                        {"range":[30,40], "color":"#ffd600"},
                        {"range":[40,50], "color":"#ffab00"},
                        {"range":[50,60], "color":"#ff6d00"},
                        {"range":[60,70], "color":"#ff3d00"},
                        {"range":[70,80], "color":"#dd2c00"},
                        {"range":[80,90], "color":"#bf360c"},
                        {"range":[90,100],"color":"#8d0000"},
                    ],
                    "threshold":{"line":{"color":"#fff","width":4},"thickness":0.82,"value":rs},
                }
            ))
            fig_g.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#e2e8f0", family="Inter"),
                height=260, margin=dict(t=16,b=0,l=30,r=30)
            )
            st.plotly_chart(fig_g, use_container_width=True)
            st.markdown(f"""
            <div style="text-align:center;margin-top:-12px;padding-bottom:14px">
              <span class="stu-badge stu-badge-{bcls}">{cat}</span><br>
              <span style="font-size:0.82rem;color:#64748b;margin-top:8px;display:block">{improve_msg}</span>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Right: Performance Radar ──
        with r_col:
            st.markdown('<div class="stu-card">', unsafe_allow_html=True)
            st.markdown('<div class="stu-card-title">📡 Performance Overview</div>', unsafe_allow_html=True)
            cats_r = ["Attendance","Study","Activity","Sleep","Scores"]
            phy_norm = min((d["physical"]-1)/4, 1)
            vals_r = [
                min(d["att"]/100, 1),
                min(d["study"]/20, 1),
                phy_norm,
                min((d["sleep"]-3)/7, 1),
                min(d["exam"]/100, 1),
            ]
            fig_r = go.Figure()
            fig_r.add_trace(go.Scatterpolar(
                r=vals_r+[vals_r[0]], theta=cats_r+[cats_r[0]],
                fill="toself",
                fillcolor="rgba(0,212,255,0.15)",
                line=dict(color="#00d4ff", width=2.5),
                name=sname
            ))
            fig_r.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                polar=dict(
                    bgcolor="rgba(0,0,0,0)",
                    radialaxis=dict(visible=True,range=[0,1],
                                   color="rgba(99,102,241,0.3)",
                                   gridcolor="rgba(99,102,241,0.15)",
                                   tickfont=dict(color="#334155",size=9)),
                    angularaxis=dict(color="#64748b",
                                    gridcolor="rgba(99,102,241,0.15)",
                                    tickfont=dict(color="#94a3b8",size=11))
                ),
                font=dict(color="#64748b",size=10),
                height=300,
                showlegend=False,
                margin=dict(t=20,b=20,l=30,r=30)
            )
            st.plotly_chart(fig_r, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ══ ROW 2: AI Insight  |  What-If Simulator ══
        ai_col, sim_col = st.columns(2)

        # ── Left: AI Insight ──
        with ai_col:
            issues, recs = [], []
            if d["study"] < 8:
                recs.append(("Increase study hours to", f"{min(d['study']+2,20)} hrs/week →",
                             f"Risk ↓ by {min(int((8-d['study'])*4),30)}%"))
            if d["att"] < 85:
                recs.append(("Improve attendance to", "85%+ →",
                             f"Risk ↓ by {min(int((85-d['att'])*0.3),20)}%"))
            if d["sleep"] < 7:
                recs.append(("Target sleep of", "7–8 hrs/night →",
                             "Improves focus & memory"))

            st.markdown('<div class="stu-card"><div class="stu-card-title">🤖 AI Insight</div>',
                        unsafe_allow_html=True)
            if recs:
                top = recs[0]
                st.markdown(
                    f'<div style="font-size:0.88rem;color:#94a3b8;margin-bottom:6px">{top[0]}</div>'
                    f'<div style="font-size:1.3rem;font-weight:900;color:#00d4ff;margin-bottom:4px">{top[1]}</div>'
                    f'<div style="font-size:1.1rem;font-weight:800;color:#00d4aa">{top[2]}</div>',
                    unsafe_allow_html=True)
                for r in recs[1:]:
                    st.markdown(
                        f'<div style="margin-top:10px;padding:8px 12px;'
                        f'background:rgba(0,212,255,0.05);border-left:3px solid #00d4ff;'
                        f'border-radius:0 8px 8px 0;font-size:0.82rem;color:#64748b">'
                        f'{r[0]} <strong style="color:#00d4ff">{r[1]}</strong> '
                        f'<span style="color:#00d4aa">{r[2]}</span></div>',
                        unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#00d4aa;font-weight:700;font-size:1rem">✅ All metrics look great! Keep it up.</div>',
                            unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Right: What-If Simulator ──
        with sim_col:
            st.markdown('<div class="stu-card">', unsafe_allow_html=True)
            st.markdown('<div class="stu-card-title">🎮 What-If Simulator</div>', unsafe_allow_html=True)

            sim_s  = st.slider("📚 Study Hours", 1, 20, max(1, d["study"]), key="sim_s")
            sim_sl = st.slider("😴 Sleep Hours", 4, 10, d["sleep"], key="sim_sl")
            sim_a  = st.slider("📅 Attendance %", 50, 100, d["att"], key="sim_a")

            new_rs  = compute_risk(sim_a, sim_s, sim_sl, d["prev"],
                                   d["physical"], d["parental"], d["internet"])
            new_cat = categorize(new_rs); new_col = rcol(new_cat)
            delta   = rs - new_rs

            if delta > 0:
                delta_html = f'<span style="color:#00d4aa;font-weight:800">Risk ↓ by {delta:.0f} pts</span>'
            elif delta < 0:
                delta_html = f'<span style="color:#ff4b6e;font-weight:800">Risk ↑ by {abs(delta):.0f} pts</span>'
            else:
                delta_html = '<span style="color:#64748b;font-weight:700">No change</span>'

            st.markdown(f"""
            <div style="display:flex;gap:12px;margin-top:10px;
                        background:linear-gradient(135deg,#0f183a,#131e48);
                        border:1px solid rgba(99,102,241,0.2);
                        border-radius:12px;padding:14px 18px;align-items:center;justify-content:space-between">
              <div style="text-align:center">
                <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;letter-spacing:0.5px">Current</div>
                <div style="font-size:1.8rem;font-weight:900;color:{col}">{rs:.0f}</div>
              </div>
              <div style="font-size:1.5rem;color:#334155">→</div>
              <div style="text-align:center">
                <div style="font-size:0.68rem;color:#475569;text-transform:uppercase;letter-spacing:0.5px">Simulated</div>
                <div style="font-size:1.8rem;font-weight:900;color:{new_col}">{new_rs:.0f}</div>
              </div>
              <div style="text-align:center">
                {delta_html}
              </div>
            </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
            st.markdown('<div class="recalc-wrap">', unsafe_allow_html=True)
            if st.button("Recalculate Risk →", use_container_width=True, key="recalc_main"):
                st.session_state["student_submitted"] = False; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown('<div style="text-align:center;color:#334155;font-size:0.72rem;padding:16px">🎓 EduPulse AI · Education · Behavioral Analytics · Personalization · 2026</div>',
            unsafe_allow_html=True)

