"""
AfriBench v1 Specification

Defines the benchmark matrix for candidate generation.
"""

DOMAINS = [
    "finance",
    "agriculture",
    "healthcare",
    "education",
    "government",
    "climate",
    "small_business",
    "language",
]

LANGUAGES = [
    "en",
    "sw",
    "ki",
    "luo",
    "sheng",
]

DIFFICULTIES = [
    "easy",
    "medium",
    "hard",
    "expert",
]

SKILLS = [
    "reasoning",
    "translation",
    "comparison",
    "planning",
    "classification",
    "summarization",
    "problem_solving",
    "explanation",
]
PILOT_DOMAINS = ["finance", "agriculture"]
PILOT_LANGUAGES = ["en", "sw"]
PILOT_DIFFICULTIES = ["easy", "hard"]
PILOT_SKILLS = ["reasoning", "translation"]