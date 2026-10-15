
import streamlit as st
from google import genai


def generate_cv_improvements(cv_text, job_description):
    """Generate CV improvement suggestions using Gemini."""

    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key not found. Please configure Streamlit Secrets."

    if not cv_text or not cv_text.strip():
        return "Please upload a CV with readable text."

    if not job_description or not job_description.strip():
        return "Please enter a job description."

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are a professional CV and ATS optimization assistant.

Analyze the CV against the target job description.

Provide:
1. Overall CV improvement recommendations.
2. Relevant keywords from the job description that are missing.
3. Suggestions to improve the professional summary.
4. Improvements for experience and project descriptions.
5. ATS formatting and readability recommendations.
6. Three specific, actionable next steps.

Important:
- Do not invent qualifications, skills, experience, or achievements.
- Clearly label suggestions that require the candidate to verify facts.
- Use simple, professional English.
- Protect personal information and do not repeat contact details.

CV TEXT:
{cv_text[:12000]}

JOB DESCRIPTION:
{job_description[:8000]}
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if response.text:
            return response.text

        return "Gemini did not return any suggestions. Please try again."

    except Exception:
        return (
            "Could not generate CV suggestions. Please check your "
            "Gemini API key, model availability, API limits, and try again."
        )
