
    
  
import html
import json
import re
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.pdf_parser import extract_text_from_pdf
from src.skill_extractor import find_skills
from src.matching import calculate_similarity
from ai_cv_improver import generate_cv_improvements

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SkillMatch AI | Career Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- THEME ----------------
if "ui_theme" not in st.session_state:
    st.session_state.ui_theme = "Light"

theme = st.session_state.ui_theme
if theme == "Dark":
    BG = "#071A12"
    PANEL = "#0E261A"
    PANEL_2 = "#163B27"
    TEXT = "#E9F8EE"
    MUTED = "#A8CBB4"
    BORDER = "#28543A"
    INPUT = "#0B2116"
    ACCENT = "#86E3A4"
else:
    BG = "#F2FAF4"
    PANEL = "#FFFFFF"
    PANEL_2 = "#DFF4E5"
    TEXT = "#173A27"
    MUTED = "#557461"
    BORDER = "#C7E5D0"
    INPUT = "#FFFFFF"
    ACCENT = "#187344"

st.markdown(
    f"""
    <style>
    :root {{
      --sm-bg: {BG}; --sm-panel: {PANEL}; --sm-panel2: {PANEL_2};
      --sm-text: {TEXT}; --sm-muted: {MUTED}; --sm-border: {BORDER};
      --sm-accent: {ACCENT}; --sm-input: {INPUT};
    }}
    .stApp {{
      background: radial-gradient(circle at 5% 0%, {PANEL_2} 0%, {BG} 45%);
      color: var(--sm-text);
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ max-width: 1400px; padding-top: 1.5rem; padding-bottom: 3rem; }}
    h1, h2, h3, h4, p, label, .stMarkdown, [data-testid="stCaptionContainer"] {{
      color: var(--sm-text);
    }}
    .hero {{
      background: linear-gradient(115deg, #0B4228 0%, #16834A 52%, #63C982 100%);
      border-radius: 24px; padding: 30px 34px; margin-bottom: 20px;
      box-shadow: 0 16px 45px rgba(18, 112, 62, .20);
    }}
    .hero h1 {{ color: #FFFFFF !important; font-size: 2.35rem; margin: 0 0 8px 0; }}
    .hero p {{ color: #F0EDFF !important; margin: 0; font-size: 1.02rem; }}
    .eyebrow {{ color: #DDFBE5 !important; text-transform: uppercase; letter-spacing: .12em;
      font-size: .75rem; font-weight: 800; margin-bottom: 10px; }}
    .panel {{
      background: var(--sm-panel); border: 1px solid var(--sm-border);
      border-radius: 18px; padding: 20px 22px; margin: 8px 0 16px 0;
      box-shadow: 0 7px 22px rgba(15, 25, 60, .05);
    }}
    .metric {{
      background: var(--sm-panel); border: 1px solid var(--sm-border);
      border-radius: 17px; padding: 18px; min-height: 128px;
    }}
    .metric-label {{ color: var(--sm-muted) !important; font-size: .85rem; font-weight: 650; }}
    .metric-value {{ color: var(--sm-accent) !important; font-size: 2rem; font-weight: 850; margin-top: 6px; }}
    .metric-foot {{ color: var(--sm-muted) !important; font-size: .77rem; margin-top: 4px; }}
    .pill {{ display:inline-block; padding:5px 10px; border-radius:99px; margin:3px 4px 3px 0;
      background: var(--sm-panel2); color: var(--sm-text); border:1px solid var(--sm-border);
      font-size:.83rem; }}
    .good {{ color:#16A36A !important; font-weight:700; }}
    .warn {{ color:#D99018 !important; font-weight:700; }}
    .bad {{ color:#E45C73 !important; font-weight:700; }}
    .muted {{ color: var(--sm-muted) !important; }}
    .stButton > button {{ border-radius: 11px; font-weight: 700; min-height: 42px; }}
    .stButton > button[kind="primary"] {{
      background: linear-gradient(100deg, #176B3D, #36A85D); color: white; border: 0;
    }}

