
from src.skill_extractor import find_skills


def test_python_skill_is_detected():
    result = find_skills("I have experience with Python.")

    assert "Programming Languages" in result
    assert "Python" in result["Programming Languages"]


def test_empty_text_returns_empty_dictionary():
    assert find_skills("") == {}


def test_unknown_skill_is_not_added():
    result = find_skills(
        "I have experience with an unknown technology."
    )

    all_skills = {
        skill
        for skills in result.values()
        for skill in skills
    }

    assert "Unknown Technology" not in all_skills


def test_skill_category_is_returned():
    result = find_skills("I use React and GitHub.")

    assert "Web Development" in result
    assert "Tools and DevOps" in result
