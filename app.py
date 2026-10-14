
import json
import streamlit as st
import pandas as pd
import plotly.express as px

from src.pdf_parser import extract_text_from_pdf
from src.skill_extractor import find_skills
from src.matching import calculate_similarity


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="SkillMatch AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- COLORFUL DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #F8F7FF 0%, #F0F4FF 100%);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(120deg, #6548E8, #9775F8, #4C8DFF);
    padding: 32px;
    border-radius: 22px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 8px 25px rgba(101, 72, 232, 0.18);
}

.hero h1 {
    color: white !important;
    font-size: 38px;
    margin-bottom: 8px;
}

.hero p {
    color: #F4F0FF;
    font-size: 16px;
}

.metric-card {
    background: white;
    border: 1px solid #E6E1FF;
    border-radius: 18px;
    padding: 20px;
    min-height: 130px;
    box-shadow: 0 4px 16px rgba(70, 50, 130, 0.06);
}

.metric-label {
    color: #6D6687;
    font-size: 14px;
    margin-bottom: 10px;
}

.metric-value {
    color: #5E46D8;
    font-size: 30px;
    font-weight: 750;
}

.section-card {
    background: white;
    border: 1px solid #E8E4F7;
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
}

.small-note {
    color: #706987;
    font-size: 13px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #7657F6, #5388F7);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 650;
    min-height: 44px;
}

div.stButton > button {
    border-radius: 10px;
}

[data-testid="stSidebar"] {
    background: #F0EDFF;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>🎯 SkillMatch AI</h1>
    <p>Your smart career companion. Discover your strengths,
    explore skill gaps, and prepare for your next opportunity.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("## 💜 SkillMatch AI")
st.sidebar.caption("SMART CAREER ANALYZER")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Dashboard", "📊 Analysis Results", "ℹ️ About Project"]
)

st.sidebar.divider()
st.sidebar.markdown("### ✨ Quick actions")

if st.sidebar.button("🧹 Clear analysis", use_container_width=True):
    st.session_state.analysis = None
    st.rerun()

st.sidebar.markdown(
    "<p class='small-note'>Your CV is processed in memory. "
    "This demo does not save uploaded CVs to a database.</p>",
    unsafe_allow_html=True
)


# ---------------- DASHBOARD PAGE ----------------

if page == "🏠 Dashboard":

    st.subheader("🚀 Analyze your CV")
    st.write(
        "Upload your resume and compare it with a job description."
    )

    col1, col2 = st.columns([1, 1.3], gap="large")

    with col1:
        st.markdown("### 📄 Your Resume")

        uploaded_file = st.file_uploader(
            "Choose your CV (PDF)",
            type=["pdf"],
            help="Upload a text-based PDF resume."
        )

        if uploaded_file:
            st.success(f"Ready to analyze: {uploaded_file.name}")
        else:
            st.info("Upload a PDF to get started.")

    with col2:
        st.markdown("### 💼 Target Job")

        sample_job = (
            "Software Engineer. Required skills: Python, JavaScript, "
            "React, SQL, Git, Docker, REST API, Machine Learning, "
            "Unit Testing and AWS."
        )

        if st.button("✨ Load sample job description"):
            st.session_state.job_description = sample_job

        job_description = st.text_area(
            "Paste the job description",
            key="job_description",
            height=180,
            placeholder=(
                "Paste the responsibilities, qualifications "
                "and technical skills from a job vacancy..."
            )
        )

    st.markdown("---")

    analyze_col, hint_col = st.columns([1, 2])

    with analyze_col:
        analyze_clicked = st.button(
            "🔍 Analyze My CV",
            type="primary",
            use_container_width=True
        )

    with hint_col:
        st.caption(
            "💡 Tip: Use a complete job description for "
            "more informative comparison results."
        )

    if analyze_clicked:

        if uploaded_file is None:
            st.warning("Please upload your CV first.")

        elif not job_description.strip():
            st.warning("Please enter a job description.")

        else:
            with st.spinner("✨ Analyzing your CV..."):

                cv_text, error = extract_text_from_pdf(uploaded_file)

                if error:
                    st.error(error)

                else:
                    cv_skills = find_skills(cv_text)
                    job_skills = find_skills(job_description)

                    cv_set = {
                        skill
                        for skills in cv_skills.values()
                        for skill in skills
                    }

                    job_set = {
                        skill
                        for skills in job_skills.values()
                        for skill in skills
                    }

                    matched = sorted(cv_set & job_set)
                    missing = sorted(job_set - cv_set)

                    coverage = (
                        len(matched) / len(job_set) * 100
                        if job_set else 0.0
                    )

                    similarity = calculate_similarity(
                        cv_text, job_description
                    )

                    st.session_state.analysis = {
                        "cv_text": cv_text,
                        "cv_skills": cv_skills,
                        "job_skills": job_skills,
                        "matched": matched,
                        "missing": missing,
                        "coverage": coverage,
                        "similarity": similarity,
                        "job_description": job_description,
                        "filename": uploaded_file.name,
                    }

                    st.success(
                        "Analysis complete! Open Analysis Results "
                        "from the sidebar to explore your results."
                    )


# ---------------- RESULTS PAGE ----------------

elif page == "📊 Analysis Results":

    result = st.session_state.analysis

    if result is None:
        st.info(
            "No analysis yet. Go to Dashboard, upload your CV, "
            "and click Analyze My CV."
        )

    else:
        st.subheader("📊 Your Analysis Dashboard")
        st.caption(f"Resume analyzed: {result['filename']}")

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🎯 CV–Job Similarity</div>
                <div class="metric-value">{result['similarity']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">✅ Matching Skills</div>
                <div class="metric-value">{len(result['matched'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📚 Skill Coverage</div>
                <div class="metric-value">{result['coverage']:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.caption(
            "Similarity measures text overlap. Skill coverage measures "
            "the share of detected job-description skills found in "
            "the CV. Neither score predicts hiring success."
        )

        st.markdown("---")

        left, right = st.columns(2, gap="large")

        with left:
            st.markdown("### ✅ Matching Skills")

            if result["matched"]:
                for skill in result["matched"]:
                    st.markdown(f"- 🟢 {skill}")
            else:
                st.info("No matching skills detected.")

        with right:
            st.markdown("### 🧩 Skills to Review")

            if result["missing"]:
                for skill in result["missing"]:
                    st.markdown(f"- 🟠 {skill}")
            else:
                st.success("All detected job skills were found.")

        st.markdown("---")
        st.markdown("### 📈 Skill Category Breakdown")

        category_rows = []

        for category, skills in result["job_skills"].items():
            matched_count = sum(
                skill in result["matched"] for skill in skills
            )

            category_rows.append({
                "Category": category,
                "Matched": matched_count,
                "Not detected": len(skills) - matched_count,
            })

        if category_rows:
            chart_data = pd.DataFrame(category_rows)

            chart_data = chart_data.melt(
                id_vars="Category",
                var_name="Status",
                value_name="Number of Skills"
            )

            fig = px.bar(
                chart_data,
                x="Category",
                y="Number of Skills",
                color="Status",
                barmode="stack",
                color_discrete_map={
                    "Matched": "#7657F6",
                    "Not detected": "#FFAD66",
                },
                title="Detected Job Skills by Category"
            )

            fig.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font_color="#332B55",
                legend_title_text="Skill status",
                xaxis_title="",
                yaxis_title="Number of skills",
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(
                "No known skills were detected in the job description. "
                "Try a description containing technical skills."
            )

        st.markdown("### 💡 Improvement Suggestions")

        if result["missing"]:
            st.write(
                "Review the following skills and add relevant evidence "
                "to your CV only if you genuinely have the experience:"
            )

            for skill in result["missing"]:
                st.markdown(f"- Learn or review **{skill}**.")
        else:
            st.write(
                "Review whether your CV clearly demonstrates the "
                "skills required for this role."
            )

        with st.expander("📄 View extracted CV text"):
            st.text(result["cv_text"])

        report = [
            "SKILLMATCH AI - CV ANALYSIS REPORT",
            f"Resume: {result['filename']}",
            f"CV-Job Similarity: {result['similarity']:.2f}%",
            f"Skill Coverage: {result['coverage']:.2f}%",
            "",
            "MATCHING SKILLS:",
            *result["matched"],
            "",
            "SKILLS TO REVIEW:",
            *result["missing"],
            "",
            "Note: Scores are text-based indicators, not hiring predictions.",
        ]

        st.download_button(
            "📥 Download Analysis Report",
            data="\n".join(report),
            file_name="skillmatch_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )


# ---------------- ABOUT PAGE ----------------

else:
    st.subheader("ℹ️ About SkillMatch AI")

    st.markdown("""
    <div class="section-card">
        <h3>💜 Our Mission</h3>
        <p>Help job seekers compare their resumes with job
        requirements and identify skills they may need to highlight
        or develop.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🛠️ Technologies Used")

    st.write(
        "Python · Streamlit · PyMuPDF · NLP · "
        "Scikit-learn · Pandas · Plotly"
    )

    st.markdown("### ⚠️ Limitations")

    st.write(
        "The current version uses a predefined skills dictionary "
        "and TF-IDF text similarity. It may miss synonyms, context "
        "and skills expressed in different ways. Missing skills "
        "mean 'not detected', not necessarily 'not possessed'."
    )

    st.markdown("### 🔒 Privacy")

    st.write(
        "The application processes the uploaded PDF during the "
        "current session. Avoid uploading confidential CVs to "
        "public demos. This app does not intentionally persist "
        "CVs, but hosting and platform logs should also be reviewed."
    )
