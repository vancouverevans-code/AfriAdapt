"""
Validate generated responses.
"""

import re


MIN_WORDS = 60
MAX_WORDS = 250


def validate_response(text: str):

    if not text:
        return False

    words = len(text.split())

    if words < MIN_WORDS:
        return False

    if words > MAX_WORDS:
        return False

    if "```" in text:
        return False

    if "# " in text:
        return False

    banned = [
        "As an AI",
        "language model",
        "I cannot",
    ]

    lower = text.lower()

    for phrase in banned:
        if phrase.lower() in lower:
            return False

    # Detect obvious repeated words
    if re.search(r"\b(\w+)\s+\1\b", lower):
        return False

    return True