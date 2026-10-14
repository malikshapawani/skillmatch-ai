
import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_FILE = PROJECT_ROOT / "data" / "skills.json"


def load_skills():
    """Load categorized skills from the JSON file."""

    with open(SKILLS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def find_skills(text):
    """Find known skills in text without matching partial words."""

    if not text:
        return {}

    skills_data = load_skills()
    text_lower = text.lower()
    found = {}

    for category, skills in skills_data.items():
        matched = []

        for skill in skills:
            pattern = (
                r"(?<!\w)"
                + re.escape(skill.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):
                matched.append(skill)

        if matched:
            found[category] = matched

    return found
