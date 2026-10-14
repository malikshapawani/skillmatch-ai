
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(cv_text, job_text):
    """Calculate text similarity between a CV and a job description."""

    if not cv_text.strip() or not job_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    try:
        vectors = vectorizer.fit_transform(
            [cv_text, job_text]
        )

        score = cosine_similarity(
            vectors[0:1], vectors[1:2]
        )[0][0]

        return round(float(score) * 100, 2)

    except ValueError:
        return 0.0
