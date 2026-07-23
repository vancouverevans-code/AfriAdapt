"""
AfriAdapt Universal Prompt Builder

Generates structured prompts for dataset creation.
"""

import random
import uuid

from scripts.utils.knowledge_loader import load_knowledge
from scripts.utils.config import load_config

from scripts.generate.templates import (
    FINANCE_TEMPLATES,
    AGRICULTURE_TEMPLATES,
    LANGUAGE_TEMPLATES,
    COMMUNICATION_TEMPLATES,
)

# ---------------------------------------------------
# Load knowledge + configuration
# ---------------------------------------------------

knowledge = load_knowledge()
config = load_config()

# ---------------------------------------------------
# Prompt templates
# ---------------------------------------------------

TEMPLATES = {
    "finance": FINANCE_TEMPLATES,
    "agriculture": AGRICULTURE_TEMPLATES,
    "language": LANGUAGE_TEMPLATES,
    "communications": COMMUNICATION_TEMPLATES,
}


# ---------------------------------------------------
# Helpers
# ---------------------------------------------------

def generate_id():
    """Generate a unique sample ID."""
    return f"AFRI-{uuid.uuid4().hex[:8]}"


def random_language():
    return random.choice(
        config.get(
            "languages",
            ["en"],
        )
    )


def random_difficulty():
    return random.choice(
        config.get(
            "difficulty",
            ["medium"],
        )
    )


def random_reasoning():
    return random.choice(
        config.get(
            "reasoning",
            ["factual"],
        )
    )


# ---------------------------------------------------
# Prompt Builder
# ---------------------------------------------------

def build_prompt(
    domain: str,
    language: str | None = None,
):
    """
    Build one structured prompt.

    Returns a dictionary ready for record_builder.
    """

    if domain not in TEMPLATES:
        raise ValueError(
            f"Unknown domain '{domain}'"
        )

    template = random.choice(
        TEMPLATES[domain]
    )

    language = language or random_language()

    difficulty = random_difficulty()

    reasoning = random_reasoning()

    # -----------------------------
    # Finance
    # -----------------------------

    if domain == "finance":

        instruction = template.format(

            concept=random.choice(
                knowledge["finance"]
            ),

            comparison=random.choice(
                knowledge["finance"]
            ),

            persona=random.choice(
                knowledge["personas"]
            ),
        )

    # -----------------------------
    # Agriculture
    # -----------------------------

    elif domain == "agriculture":

        instruction = template.format(

            crop=random.choice(
                knowledge["agriculture"]
            ),

            disease="blight",

            fertilizer="organic fertilizer",

            weather="drought",

        )

    # -----------------------------
    # Language
    # -----------------------------

    elif domain == "language":

        instruction = template.format(

            language=random.choice(
                knowledge["languages"]
            )

        )

    # -----------------------------
    # Communications
    # -----------------------------

    elif domain == "communications":

        instruction = template.format(

            topic="AI adoption in Africa",

            product="AfriAdapt",

        )

    else:

        raise ValueError(
            f"Unsupported domain: {domain}"
        )

    return {

        "id": generate_id(),

        "domain": domain,

        "language": language,

        "difficulty": difficulty,

        "reasoning_type": reasoning,

        "instruction": instruction,

    }


# ---------------------------------------------------
# Smoke Test
# ---------------------------------------------------

if __name__ == "__main__":

    domains = config.get(
        "domains",
        [
            "finance",
            "agriculture",
            "language",
            "communications",
        ],
    )

    print("\nGenerated Samples\n")

    for domain in domains:

        sample = build_prompt(domain)

        print("=" * 60)

        for key, value in sample.items():

            print(f"{key}: {value}")

        print()