
    
  
    else:
        st.success(f"CV ready: {result['filename']}")
        st.caption(
            "Your CV text and job description will be sent to "
            "Google Gemini to generate improvement suggestions. "
            "Use a CV with personal contact details removed when testing."
        )

        if st.button(
            "✨ Improve My CV",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner("Gemini is reviewing your CV..."):
                suggestions = generate_cv_improvements(
                    result["cv_text"],
                    result["job_description"],
                )
            st.session_state["ai_cv_suggestions"] = suggestions

        suggestions = st.session_state.get("ai_cv_suggestions")
        if suggestions:
            st.markdown("### Your AI improvement recommendations")
            st.markdown(suggestions)
            st.download_button(
                "⬇️ Download AI recommendations",
                data=suggestions,
                file_name="skillmatch_ai_cv_improvements.txt",
                mime="text/plain",
                use_container_width=True,
            )

elif page == "📄 Export report":
    if not result:
        st.info("Run an analysis first from **Analyze CV**.")
    else:
        st.subheader("Export your analysis")
        st.markdown(
            '<div class="section-intro">Choose a format for your report. Review the contents before sharing, as reports may include details extracted from your CV.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="export-card">
              <span class="export-icon">📊</span>
              <h3>Detailed analysis report</h3>
              <p>Review match indicators, skill tables, and recommendations in a browser.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        html_col, txt_col = st.columns(2, gap="large")
        with html_col:
            with st.container(border=True):
                st.markdown("### 🌐 HTML report")
                st.write("A styled report with metrics, skill tables, and recommendations.")
                st.download_button(
                    "⬇️ Download HTML report",
                    data=html_report(result),
                    file_name="skillmatch_ai_report.html",
                    mime="text/html",
                    type="primary",
                    use_container_width=True,
                )
        with txt_col:
            with st.container(border=True):
                st.markdown("### 📝 Plain-text report")
                st.write("A lightweight text summary for notes and records.")
                st.download_button(
                    "⬇️ Download TXT report",
                    data=make_text_report(result),
                    file_name="skillmatch_ai_report.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
        if result["priority_rows"]:
            csv_data = pd.DataFrame(result["priority_rows"])[["Skill", "Priority", "Status"]].to_csv(index=False).encode("utf-8")
            with st.container(border=True):
                st.markdown("### 🌿 Skill-gap data")
                st.write("A CSV spreadsheet of detected skills, priorities, and match status.")
                st.download_button(
                    "⬇️ Download skill-gap CSV",
                    data=csv_data,
                    file_name="skillmatch_skill_gaps.csv",
                    mime="text/csv",
                    use_container_width=True,
                )
        st.caption("Available formats: HTML, TXT, and CSV. PDF export is not included in this version.")

elif page == "ℹ️ About":
    st.subheader("About SkillMatch AI")
    st.markdown(
        '<div class="section-intro">SkillMatch AI helps job seekers compare a text-based PDF CV with a target job description, understand detected gaps, and plan practical improvements.</div>',
        unsafe_allow_html=True,
    )
    about_left, about_right = st.columns(2, gap="large")
    with about_left:
        st.markdown(
            """
            <div class="about-card components">
              <h3>🌿 Current analysis components</h3>
              <ul>
                <li>PDF text extraction with PyMuPDF</li>
                <li>Skill dictionary matching by category</li>
                <li>TF-IDF and cosine similarity</li>
                <li>Skill coverage and missing-skill identification</li>
                <li>Heuristic ATS-readiness indicators</li>
                <li>CV section checks and improvement suggestions</li>
                <li>Interactive charts and HTML / TXT / CSV reports</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with about_right:
        st.markdown(
            """
            <div class="about-card limitations">
              <h3>⚠️ Limitations</h3>
              <ul>
                <li>Skill detection depends on <code>data/skills.json</code>; unlisted skills may be missed.</li>
                <li>Text similarity is not full semantic understanding of the job.</li>
                <li>ATS readiness is a heuristic, not a vendor ATS score.</li>
                <li>The system cannot verify truthfulness, proficiency, or work experience.</li>
                <li>Scanned PDFs without a text layer may not be readable.</li>
              </ul>
            </div>
            """,

