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
    [data-testid="stSidebar"] {{
    background: var(--sm-panel) !important;
    border-right: 1px solid var(--sm-border);
    }}
    
    [data-testid="stSidebar"] * {{
    color: var(--sm-text) !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {{
    color: var(--sm-text) !important;
    }}

    [data-testid="stFileUploader"], [data-testid="stTextArea"] {{
      background: var(--sm-panel); border-radius: 14px;
    }}
    textarea, input {{ color: var(--sm-text) !important; background: var(--sm-input, {INPUT}) !important; }}
    [data-testid="stMetric"] {{ background: var(--sm-panel); border:1px solid var(--sm-border);
      padding: 14px; border-radius: 14px; }}
    [data-testid="stDataFrame"] {{ border: 1px solid var(--sm-border); border-radius: 12px; }}
    
/* Highlight buttons */
.stButton > button {{
    background: linear-gradient(135deg, #087f5b, #20b878) !important;
    color: #ffffff !important;
    border: 1px solid #48c78e !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.65rem 1rem !important;
    box-shadow: 0 4px 12px rgba(16, 130, 82, 0.18);
    transition: all 0.2s ease-in-out;
}}

.stButton > button:hover {{
    background: linear-gradient(135deg, #066747, #16a36a) !important;
    border-color: #70e0aa !important;
    transform: translateY(-2px);
    box-shadow: 0 7px 18px rgba(16, 130, 82, 0.28);
}}

/* Highlight cards */
[data-testid="stVerticalBlockBorderWrapper"] {{
    border: 1px solid var(--sm-border) !important;
    border-radius: 16px !important;
    box-shadow: 0 5px 16px rgba(16, 100, 65, 0.08);
    transition: all 0.2s ease-in-out;
}}

[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: #39b77a !important;
    box-shadow: 0 8px 22px rgba(16, 130, 82, 0.16);
}}

/* Highlight input fields */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {{
    border: 1px solid var(--sm-border) !important;
    border-radius: 10px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: #20b878 !important;
    box-shadow: 0 0 0 3px rgba(32, 184, 120, 0.18) !important;
}}

/* Highlight dropdowns */
[data-baseweb="select"] > div {{
    border-radius: 10px !important;
    border-color: var(--sm-border) !important;
}}

[data-baseweb="select"] > div:focus-within {{
    border-color: #20b878 !important;
    box-shadow: 0 0 0 2px rgba(32, 184, 120, 0.18) !important;
}}

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- HELPERS ----------------
SECTION_PATTERNS = {
    "Contact details": [r"\bemail\b", r"\bphone\b", r"\bcontact\b", r"@[\w.-]+\.\w+"],
    "Professional summary": [r"\bsummary\b", r"\bprofile\b", r"\bobjective\b", r"\babout me\b"],
    "Work experience": [r"\bexperience\b", r"\bemployment\b", r"\bwork history\b", r"\binternship\b"],
    "Education": [r"\beducation\b", r"\bdegree\b", r"\bqualification\b", r"\buniversity\b"],
    "Projects": [r"\bprojects?\b", r"\bportfolio\b", r"\bcase studies\b"],
    "Skills": [r"\btechnical skills\b", r"\bskills\b", r"\btechnologies\b", r"\bcompetencies\b"],
    "Certifications": [r"\bcertifications?\b", r"\blicenses?\b", r"\bcredentials?\b"],
}

ACTION_VERBS = [
    "built", "developed", "designed", "implemented", "automated", "optimized",
    "created", "delivered", "improved", "analyzed", "tested", "deployed",
    "integrated", "managed", "led", "reduced", "increased", "maintained",
]

def flatten_skills(skill_dict):
    return sorted({str(skill) for values in skill_dict.values() for skill in values}, key=str.lower)

def detect_sections(cv_text):
    text = cv_text.lower()
    found = {}
    for section, patterns in SECTION_PATTERNS.items():
        found[section] = any(re.search(pattern, text) for pattern in patterns)
    return found

def ats_score(cv_text, sections):
    words = re.findall(r"\b[\w+#.-]+\b", cv_text)
    word_count = len(words)
    bullets = len(re.findall(r"(?m)^\s*(?:[-•*▪]|\d+[.)])\s+", cv_text))
    quantified = len(re.findall(r"\b\d+(?:\.\d+)?\s?(?:%|x|k|m|years?|months?|users?|clients?|projects?)?\b", cv_text.lower()))
    action_count = sum(len(re.findall(rf"\b{re.escape(v)}\b", cv_text.lower())) for v in ACTION_VERBS)
    section_count = sum(sections.values())
    score = 0
    score += min(section_count / len(SECTION_PATTERNS), 1) * 35
    score += min(word_count / 450, 1) * 15
    score += min(bullets / 8, 1) * 15
    score += min(quantified / 5, 1) * 15
    score += min(action_count / 6, 1) * 20
    return round(score), {
        "Word count": word_count,
        "Bullet points detected": bullets,
        "Quantified results detected": quantified,
        "Action verbs detected": action_count,
        "Sections detected": section_count,
    }

def prioritize_skills(job_text, job_skills, cv_skills):
    lower = job_text.lower()
    cv_set = set(cv_skills)
    rows = []
    for skill in job_skills:
        escaped = re.escape(skill.lower())
        positions = [m.start() for m in re.finditer(escaped, lower)]
        context = " ".join(lower[max(0, p - 70):p + len(skill) + 70] for p in positions)
        if any(word in context for word in ["required", "must have", "mandatory", "essential", "need to have"]):
            priority = "High"
            weight = 3
        elif any(word in context for word in ["preferred", "bonus", "nice to have", "plus", "desirable"]):
            priority = "Low"
            weight = 1
        else:
            priority = "Medium"
            weight = 2
        rows.append({
            "Skill": skill,
            "Priority": priority,
            "Status": "Matched" if skill in cv_set else "Missing",
            "Weight": weight,
        })
    return rows

def build_recommendations(result):
    recs = []
    missing = result["missing"]
    sections = result["sections"]
    if not sections.get("Professional summary", False):
        recs.append(("High", "Add a short professional summary", "Write 2–3 lines tailored to the target role and include your strongest relevant skills."))
    if not sections.get("Projects", False):
        recs.append(("High", "Add a Projects section", "Include 2–3 relevant projects, your role, tools used, and the outcome."))
    if not sections.get("Education", False):
        recs.append(("Medium", "Make Education easy to find", "Add your degree, institution, graduation year, and relevant coursework if useful."))
    if not sections.get("Certifications", False):
        recs.append(("Low", "Add relevant certifications if you have them", "Only list genuine certificates that support the target role."))
    if result["ats_score"] < 70:
        recs.append(("High", "Improve ATS readability", "Use standard section headings, simple formatting, and concise bullet points. Avoid relying on graphics to convey essential details."))
    if result["quantified"] < 2:
        recs.append(("Medium", "Show measurable outcomes", "Where accurate, add numbers such as time saved, users supported, test coverage, or project scope. Do not invent metrics."))
    for skill in missing[:5]:
        recs.append(("High" if skill in result["high_priority_missing"] else "Medium",
                     f"Address the skill gap: {skill}",
                     f"If you genuinely have this experience, make it easier to find in your CV. Otherwise, plan a small project or course to build evidence for {skill}."))
    if not recs:
        recs.append(("Low", "Keep tailoring your CV", "Your basic structure looks complete. Continue aligning examples and project evidence with each vacancy."))
    return recs

def make_text_report(result):
    lines = [
        "SKILLMATCH AI — CAREER ANALYSIS REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"CV: {result['filename']}",
        "",
        f"Text similarity: {result['similarity']:.1f}%",
        f"Skill coverage: {result['coverage']:.1f}%",
        f"ATS-readiness estimate: {result['ats_score']}/100",
        f"Matched skills: {len(result['matched'])}",
        f"Missing skills: {len(result['missing'])}",
        "",
        "MATCHED SKILLS",
        *([f"- {s}" for s in result["matched"]] or ["- None detected"]),
        "",
        "MISSING SKILLS",
        *([f"- {s}" for s in result["missing"]] or ["- None detected"]),
        "",
        "SECTION CHECK",
        *[f"- {name}: {'Found' if found else 'Not detected'}" for name, found in result["sections"].items()],
        "",
        "RECOMMENDATIONS",
        *[f"- [{priority}] {title}: {detail}" for priority, title, detail in result["recommendations"]],
        "",
        "Note: These are heuristic analysis indicators, not a hiring decision or a guarantee of ATS performance.",
    ]
    return "\n".join(lines)

def html_report(result):
    rows = "".join(
        f"<tr><td>{html.escape(r['Skill'])}</td><td>{r['Priority']}</td><td>{r['Status']}</td></tr>"
        for r in result["priority_rows"]
    )
    recs = "".join(
        f"<li><b>[{html.escape(p)}] {html.escape(t)}</b><br>{html.escape(d)}</li>"
        for p, t, d in result["recommendations"]
    )
    matched = ", ".join(result["matched"]) or "None detected"
    missing = ", ".join(result["missing"]) or "None detected"
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>SkillMatch AI report</title>
    <style>body{{font:16px Arial;max-width:900px;margin:40px auto;padding:0 20px;color:#20243a}}
    h1{{color:#176B3D}}.cards{{display:flex;gap:12px;flex-wrap:wrap}}.card{{padding:18px;border:1px solid #C7E5D0;border-radius:12px;min-width:170px}}
    table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:9px;text-align:left}}th{{background:#DFF4E5}}
    .note{{color:#666;font-size:13px}}</style></head><body>
    <h1>🎯 SkillMatch AI</h1><h2>Career Analysis Report</h2>
    <p><b>CV:</b> {html.escape(result['filename'])} &nbsp; <b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    <div class="cards"><div class="card"><b>Text similarity</b><h2>{result['similarity']:.1f}%</h2></div>
    <div class="card"><b>Skill coverage</b><h2>{result['coverage']:.1f}%</h2></div>
    <div class="card"><b>ATS-readiness estimate</b><h2>{result['ats_score']}/100</h2></div></div>
    <h2>Matched skills</h2><p>{html.escape(matched)}</p><h2>Missing skills</h2><p>{html.escape(missing)}</p>
    <h2>Skill-by-skill analysis</h2><table><tr><th>Skill</th><th>Priority</th><th>Status</th></tr>{rows}</table>
    <h2>Recommendations</h2><ol>{recs}</ol>
    <p class="note">These are heuristic indicators, not a hiring decision or a guarantee of ATS performance. Only claim skills and results you can honestly demonstrate.</p>
    </body></html>"""

def chart_layout(fig):
    fig.update_layout(
        paper_bgcolor=PANEL, plot_bgcolor=PANEL, font_color=TEXT,
        margin=dict(l=10, r=10, t=35, b=10), legend_title_text="",
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig



# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🎯 SkillMatch AI")
    st.caption("CAREER INTELLIGENCE WORKSPACE")

    page = st.radio(
        "Workspace",
        [
            "🏠 Overview",
            "🔎 Analyze CV",
            "📊 Insights",
            "🧭 Action plan",
            "✨ AI CV Improvement",
            "📄 Export report",
            "ℹ️ About",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("### Appearance")
    st.selectbox(
        "Choose theme",
        ["Light", "Dark"],
        key="ui_theme",
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("**Analysis workflow**")
    st.caption(
        "1. Upload CV PDF\n\n"
        "2. Paste the target job\n\n"
        "3. Analyze gaps\n\n"
        "4. Export your report"
    )

    if st.button("Reset current analysis", use_container_width=True):
        st.session_state.analysis = None
        st.rerun()

    st.caption(
        "Privacy: this demo processes the uploaded PDF in app memory "
        "and does not intentionally save it to a database."
    )

# ---------------- HERO ----------------
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">CAREER INTELLIGENCE • CV OPTIMIZATION</div>
      <h1>SkillMatch AI</h1>
      <p>Understand your fit, discover skill gaps, and turn your resume into a stronger application.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

result = st.session_state.get("analysis")

if page == "🏠 Overview":
    st.subheader("Your career workspace")
    st.write("A structured review of your CV against a target vacancy — with evidence, gaps, and practical next steps.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="panel"><h3>🎯 Match intelligence</h3><p class="muted">Compare text similarity with detected skill coverage instead of relying on one number.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel"><h3>🧩 Gap prioritization</h3><p class="muted">Separate high-priority requirements from preferred skills and see what to address first.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="panel"><h3>🚀 Improvement plan</h3><p class="muted">Get section checks, evidence-based suggestions, and an exportable report.</p></div>', unsafe_allow_html=True)
    if result:
        st.success(f"Latest analysis available for **{result['filename']}**.")
        a, b, c, d = st.columns(4)
        a.metric("Text similarity", f"{result['similarity']:.1f}%")
        b.metric("Skill coverage", f"{result['coverage']:.1f}%")
        c.metric("ATS readiness", f"{result['ats_score']}/100")
        d.metric("Missing skills", len(result["missing"]))
        st.info("Open Insights or Action plan in the sidebar to continue.")
    else:
        st.info("Start in **Analyze CV** to upload a PDF and paste a job description.")
    st.markdown("#### What the scores mean")
    st.markdown(
        "- **Text similarity:** lexical overlap estimated using TF-IDF; it is not a semantic understanding score.\n"
        "- **Skill coverage:** share of detected job skills also found in the CV.\n"
        "- **ATS-readiness estimate:** a transparent heuristic based on sections, length, bullets, action verbs, and measurable evidence — not a real ATS vendor score."
    )

elif page == "🔎 Analyze CV":
    st.subheader("Analyze a resume against a vacancy")
    st.caption("Use a text-based PDF. Scanned image PDFs may need OCR before analysis.")
    left, right = st.columns([0.9, 1.1], gap="large")
    with left:
        uploaded_file = st.file_uploader("Upload your CV (PDF)", type=["pdf"], help="Your file is processed for this session.")
        if uploaded_file:
            st.success(f"Ready: {uploaded_file.name}")
        st.markdown("#### Job description")
        sample_job = (
            "Software Engineer\n\n"
            "Required: Python, SQL, Git, REST API, unit testing, problem solving.\n"
            "Responsibilities: Develop and maintain web applications, design APIs, "
            "write automated tests, collaborate with a team, review code, and document solutions.\n"
            "Preferred: Docker, AWS, CI/CD, React, machine learning."
        )
        if st.button("Load a realistic sample job", use_container_width=True):
            st.session_state.job_description = sample_job
        job_description = st.text_area(
            "Paste the complete job description",
            key="job_description",
            height=260,
            placeholder="Include responsibilities, required qualifications, preferred skills, and experience...",
        )
        analyze = st.button("✨ Run full analysis", type="primary", use_container_width=True)
    with right:
        st.markdown("#### What you'll receive")
        st.markdown(
            "- Overall match indicators and a transparent ATS-readiness estimate\n"
            "- Required / preferred skill gap table\n"
            "- CV section completeness check\n"
            "- Category-level skill coverage visualization\n"
            "- Specific suggestions to improve the CV\n"
            "- Downloadable HTML report and plain-text summary"
        )
        st.warning("The analyzer identifies terms and structural signals. It cannot verify whether a skill is genuinely mastered, and it does not predict hiring outcomes.")
        st.markdown("#### Privacy reminder")
        st.caption("Avoid uploading another person's CV without permission. Remove sensitive information if it is not needed for analysis.")

    if analyze:
        if uploaded_file is None:
            st.warning("Please upload a PDF CV first.")
        elif not job_description.strip():
            st.warning("Please enter a job description.")
        else:
            with st.spinner("Reading CV and building your analysis..."):
                cv_text, error = extract_text_from_pdf(uploaded_file)
                if error:
                    st.error(error)
                else:
                    cv_skill_map = find_skills(cv_text)
                    job_skill_map = find_skills(job_description)
                    cv_skills = flatten_skills(cv_skill_map)
                    job_skills = flatten_skills(job_skill_map)
                    cv_set = set(cv_skills)
                    job_set = set(job_skills)
                    matched = sorted(cv_set & job_set, key=str.lower)
                    missing = sorted(job_set - cv_set, key=str.lower)
                    coverage = (len(matched) / len(job_set) * 100) if job_set else 0.0
                    similarity = calculate_similarity(cv_text, job_description)
                    sections = detect_sections(cv_text)
                    ats, metrics = ats_score(cv_text, sections)
                    priority_rows = prioritize_skills(job_description, job_skills, cv_skills)
                    high_priority_missing = [r["Skill"] for r in priority_rows if r["Status"] == "Missing" and r["Priority"] == "High"]
                    analysis = {
                        "filename": uploaded_file.name,
                        "cv_text": cv_text,
                        "job_description": job_description,
                        "cv_skill_map": cv_skill_map,
                        "job_skill_map": job_skill_map,
                        "cv_skills": cv_skills,
                        "job_skills": job_skills,
                        "matched": matched,
                        "missing": missing,
                        "coverage": coverage,
                        "similarity": similarity,
                        "sections": sections,
                        "ats_score": ats,
                        "word_count": metrics["Word count"],
                        "bullets": metrics["Bullet points detected"],
                        "quantified": metrics["Quantified results detected"],
                        "action_verbs": metrics["Action verbs detected"],
                        "priority_rows": priority_rows,
                        "high_priority_missing": high_priority_missing,
                    }
                    analysis["recommendations"] = build_recommendations(analysis)
                    st.session_state.analysis = analysis
                    st.success("Analysis complete. Open Insights, Action plan, and Export report from the sidebar.")
                    st.rerun()

elif page == "📊 Insights":
    if not result:
        st.info("Run an analysis first from **Analyze CV**.")
    else:
        st.subheader("Analysis insights")
        st.caption(f"Report for: {result['filename']}")
        a, b, c, d = st.columns(4)
        a.metric("Text similarity", f"{result['similarity']:.1f}%")
        b.metric("Skill coverage", f"{result['coverage']:.1f}%")
        c.metric("ATS readiness", f"{result['ats_score']}/100")
        d.metric("Skills matched", f"{len(result['matched'])}/{len(result['job_skills'])}")
        st.caption("Similarity and coverage measure different things. ATS readiness is a transparent heuristic, not a guarantee of passing an applicant tracking system.")
        tabs = st.tabs(["Skill gaps", "CV structure", "Skill categories", "CV text preview"])
        with tabs[0]:
            if result["priority_rows"]:
                df = pd.DataFrame(result["priority_rows"])[["Skill", "Priority", "Status"]]
                st.dataframe(df, use_container_width=True, hide_index=True)
                if result["job_skills"]:
                    matched_n = len(result["matched"])
                    missing_n = len(result["missing"])
                    fig = go.Figure(data=[
                        go.Bar(name="Matched", x=["Job skills"], y=[matched_n], marker_color="#239B62"),
                        go.Bar(name="Missing", x=["Job skills"], y=[missing_n], marker_color="#A8DDB5"),
                    ])
                    fig.update_layout(barmode="stack", title="Detected job skills: matched vs missing", yaxis_title="Number of skills")
                    st.plotly_chart(chart_layout(fig), use_container_width=True)
            else:
                st.info("No skills from the current skill dictionary were detected in the job description. You can extend data/skills.json.")
        with tabs[1]:
            section_df = pd.DataFrame([
                {"CV section": name, "Status": "Detected" if found else "Not detected", "Present": int(found)}
                for name, found in result["sections"].items()
            ])
            st.dataframe(section_df[["CV section", "Status"]], use_container_width=True, hide_index=True)
            fig = px.bar(section_df, x="CV section", y="Present", range_y=[0, 1.15], title="CV section completeness", text="Status")
            st.plotly_chart(chart_layout(fig), use_container_width=True)
            st.caption(f"Text signals: {result['word_count']} words • {result['bullets']} bullets • {result['action_verbs']} action-verb mentions • {result['quantified']} numeric evidence signals.")
        with tabs[2]:
            categories = []
            for category, skills in result["job_skill_map"].items():
                total = len(skills)
                found = sum(1 for s in skills if s in result["matched"])
                categories.append({"Category": category, "Matched": found, "Missing": total - found, "Coverage %": round(found / total * 100, 1) if total else 0})
            if categories:
                cat_df = pd.DataFrame(categories)
                st.dataframe(cat_df, use_container_width=True, hide_index=True)
                fig = px.bar(cat_df, x="Category", y=["Matched", "Missing"], barmode="group", title="Coverage by skill category")
                st.plotly_chart(chart_layout(fig), use_container_width=True)
            else:
                st.info("No categorized skills were detected.")
        with tabs[3]:
            st.text_area("Extracted CV text (read-only preview)", result["cv_text"], height=300, disabled=True)

elif page == "🧭 Action plan":
    if not result:
        st.info("Run an analysis first from **Analyze CV**.")
    else:
        st.subheader("Your prioritized improvement plan")
        st.write("Start with the highest-impact changes. Suggestions are based on detected text signals; verify each one against your actual experience.")
        for i, (priority, title, detail) in enumerate(result["recommendations"], 1):
            with st.container(border=True):
                col1, col2 = st.columns([0.18, 0.82])
                with col1:
                    if priority == "High":
                        st.error("HIGH")
                    elif priority == "Medium":
                        st.warning("MEDIUM")
                    else:
                        st.info("LOW")
                with col2:
                    st.markdown(f"**{i}. {title}**")
                    st.write(detail)
        st.markdown("#### Suggested learning focus")
        if result["missing"]:
            st.write("Review these gaps first, especially those marked High in the Insights table:")
            st.write(", ".join(result["missing"][:8]))
            st.caption("A gap means the skill was not detected in the CV text. It does not prove you lack the skill.")
        else:
            st.success("No missing skills from the current skill dictionary were detected. Review whether the CV gives concrete evidence for each requirement.")

elif page == "📄 Export report":
    if not result:
        st.info("Run an analysis first from **Analyze CV**.")
    else:
        st.subheader("Export your analysis")
        st.write("Download a shareable report for your own review. Check the report before sharing it with anyone.")
        st.download_button(
            "⬇️ Download detailed HTML report",
            data=html_report(result),
            file_name="skillmatch_ai_report.html",
            mime="text/html",
            type="primary",
            use_container_width=True,
        )
        st.download_button(
            "⬇️ Download plain-text report",
            data=make_text_report(result),
            file_name="skillmatch_ai_report.txt",
            mime="text/plain",
            use_container_width=True,
        )
        if result["priority_rows"]:
            csv_data = pd.DataFrame(result["priority_rows"])[["Skill", "Priority", "Status"]].to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download skill-gap CSV",
                data=csv_data,
                file_name="skillmatch_skill_gaps.csv",
                mime="text/csv",
                use_container_width=True,
            )
        st.caption("This version exports HTML, text, and CSV. A PDF export can be added later with a PDF-generation dependency.")

elif page == "ℹ️ About":
    st.subheader("About SkillMatch AI")
    st.write("SkillMatch AI is a resume analysis prototype designed to help job seekers compare a text-based PDF CV with a job description.")
    st.markdown("#### Current analysis components")
    st.markdown(
        "- PDF text extraction with PyMuPDF\n"
        "- Skill dictionary matching by category\n"
        "- TF-IDF and cosine similarity\n"
        "- Skill coverage and missing-skill identification\n"
        "- Heuristic ATS-readiness indicators\n"
        "- CV section checks and improvement suggestions\n"
        "- Interactive charts and downloadable HTML / TXT / CSV reports"
    )
    st.markdown("#### Limitations")
    st.markdown(
        "- Skill detection depends on `data/skills.json`; unlisted skills may be missed.\n"
        "- Text similarity is not a full semantic understanding of the job.\n"
        "- The ATS-readiness estimate is a transparent heuristic, not a vendor ATS score.\n"
        "- The system cannot verify truthfulness, proficiency, or actual work experience.\n"
        "- A scanned PDF without a text layer may not be readable."
    )
    st.info("Use the results as guidance, not as a hiring prediction. Never add skills or achievements to a CV unless they are true.")
