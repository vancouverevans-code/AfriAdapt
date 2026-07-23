"""
AfriAdapt Universal Prompt Builder
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

knowledge = load_knowledge()
config = load_config()

TEMPLATES = {
    "finance": FINANCE_TEMPLATES,
    "agriculture": AGRICULTURE_TEMPLATES,
    "language": LANGUAGE_TEMPLATES,
    "communications": COMMUNICATION_TEMPLATES,
}


def generate_id():
    return "AFRI-" + str(uuid.uuid4())[:8]


def build_prompt(domain: str):
    """
    Build one structured prompt for the given domain.
    """

    template = random.choice(TEMPLATES[domain])

    language = random.choice(config["languages"])
    difficulty = random.choice(config["difficulty"])
    reasoning = random.choice(config["reasoning"])

    # ---------- Finance ----------

    if domain == "finance":

        concept = random.choice(knowledge["finance"])
        comparison = random.choice(knowledge["finance"])
        persona = random.choice(knowledge["personas"])

        instruction = template.format(
            concept=concept,
            comparison=comparison,
            persona=persona,
        )

    # ---------- Agriculture ----------

    elif domain == "agriculture":

        crop = random.choice(knowledge["agriculture"])

        instruction = template.format(
            crop=crop,
            disease="blight",
            fertilizer="organic fertilizer",
            weather="drought",
        )

    # ---------- Language ----------

    elif domain == "language":

        instruction = template.format(
            language=random.choice(knowledge["languages"])
        )

    # ---------- Communications ----------

    elif domain == "communications":

        instruction = template.format(
            topic="AI adoption in Africa",
            product="AfriAdapt"
        )

    else:
        raise ValueError(f"Unknown domain: {domain}")

    return {
        "id": generate_id(),
        "domain": domain,
        "language": language,
        "difficulty": difficulty,
        "reasoning_type": reasoning,
        "instruction": instruction,
    }


if __name__ == "__main__":

    for domain in config["domains"]:
        print(build_prompt(domain))