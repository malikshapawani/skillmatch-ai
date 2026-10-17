# SkillMatch AI — Smart CV Analyzer

**An AI-powered career intelligence tool that helps job seekers analyze their CVs, identify skill gaps, and improve their job readiness.**

🌐 **Live Demo:** https://skillmatch-ai-demoz.streamlit.app/

💻 **GitHub Repository:** https://github.com/malikshapawani/skillmatch-ai 

## Overview

SkillMatch AI is a web application designed to help users understand how well their CVs align with a target job description. It analyzes CV content, identifies relevant skills, highlights potential skill gaps, and provides actionable recommendations to support career development.

The application combines CV analysis, visual insights, personalized action planning, and AI-assisted CV improvement in one dashboard.

## Key Features

- **CV Upload:** Upload a CV in PDF format.
- **Job Description Matching:** Compare CV content against a target job description.
- **Skill Gap Analysis:** Identify relevant skills and areas that may need improvement.
- **ATS Readiness Insights:** Review CV structure and job-related skill coverage.
- **Interactive Dashboard:** Explore analysis metrics, charts, and skill insights.
- **Personalized Action Plan:** View high-, medium-, and low-priority recommendations.
- **AI CV Improvement:** Generate relevant suggestions to improve CV content.
- **Exportable Reports:** Download analysis results in HTML, TXT, and CSV formats.
- **Light and Dark Themes:** Switch between themes for a comfortable viewing experience.

## Technology Stack

- **Frontend and Application Framework:** Streamlit
- **Programming Language:** Python
- **CV Processing:** PyMuPDF
- **Text Processing:** NLTK
- **Machine Learning and Text Similarity:** scikit-learn
- **Data Processing:** pandas
- **Data Visualization:** Plotly
- **AI Integration:** Google Gemini API
- **Testing:** pytest

## Application Workflow

1. Upload a CV.
2. Enter a target job description.
3. Run the CV analysis.
4. Review matching insights, skill coverage, and skill gaps.
5. Explore personalized recommendations.
6. Generate AI-assisted CV improvement suggestions.
7. Download the analysis reports.

## Testing and Quality Assurance

The application underwent feature testing and end-to-end smoke testing.

| Feature | Result |
|---|---|
| Action Plan | 4/4 passed |
| Export Reports | 4/4 passed |
| AI CV Improvement | 4/4 passed |
| Full Application Smoke Test | 9/9 passed |

The tested workflows included CV upload, analysis, visual insights, recommendations, report downloads, AI error handling, and Light/Dark theme readability.

## Security Considerations

- Store API credentials in Streamlit Secrets or environment variables.
- Never commit API keys or other secrets to the repository.
- Avoid uploading real CVs containing sensitive personal information when testing publicly.
- Treat AI-generated recommendations as suggestions and review them before using them in a CV.

## Future Improvements

- Expand skill extraction and job-role coverage.
- Improve CV parsing for different document formats.
- Add more detailed career-development recommendations.
- Expand automated test coverage and regression testing.
- Improve accessibility and usability based on user feedback.

## Author

**Maliksha Pawani**

Software Engineering Student | UI/UX Design | Python | AI-Powered Applications

---

*SkillMatch AI is a portfolio project focused on CV analysis, skill-gap identification, and AI-assisted career development.*
