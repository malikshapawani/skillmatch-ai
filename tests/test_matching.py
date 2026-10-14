
from src.matching import calculate_similarity


def test_identical_text_has_high_similarity():
    text = "Python developer with SQL experience"

    score = calculate_similarity(text, text)

    assert score > 99


def test_empty_cv_returns_zero():
    score = calculate_similarity(
        "",
        "Python developer with SQL experience"
    )

    assert score == 0.0


def test_empty_job_description_returns_zero():
    score = calculate_similarity(
        "Python developer with SQL experience",
        ""
    )

    assert score == 0.0


def test_similarity_is_between_zero_and_100():
    score = calculate_similarity(
        "Python developer",
        "Java software engineer"
    )

    assert 0.0 <= score <= 100.0
