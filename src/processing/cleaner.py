import re
from html import unescape


def clean_text(text: str | None) -> str:
    """Clean HTML and normalize whitespace."""

    if not text:
        return ""

    text = unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_categories(categories: list[str] | None) -> list[str]:
    """Remove empty categories and normalize whitespace."""

    if not categories:
        return []

    cleaned = []

    for category in categories:
        if not category:
            continue

        category = clean_text(category).lower().strip()

        if category:
            cleaned.append(category)

    return sorted(set(cleaned))