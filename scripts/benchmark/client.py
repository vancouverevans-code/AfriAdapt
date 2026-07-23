"""
AfriBench Benchmark Client

Builds benchmark prompts and delegates LLM generation
to the central generator.
"""

from typing import Dict

from scripts.benchmark.prompts import build_prompt
from scripts.llm.generator import generate_response
from scripts.utils.logger import logger


def generate_candidate(
    domain: str,
    language: str,
    difficulty: str,
    skill: str,
) -> Dict:
    """
    Generate a single benchmark candidate.

    Parameters
    ----------
    domain
        Benchmark domain.

    language
        Target language.

    difficulty
        Difficulty level.

    skill
        Reasoning skill.

    Returns
    -------
    dict
        Parsed benchmark candidate.
    """

    logger.info(
        "Benchmark Candidate | %s | %s | %s | %s",
        domain,
        language,
        difficulty,
        skill,
    )

    prompt = build_prompt(
        domain,
        language,
        difficulty,
        skill,
    )

    record = {

        "domain": domain,

        "instruction": prompt,

        "metadata": {

            "domain": domain,

            "language": language,

            "difficulty": difficulty,

            "skill": skill,

        }

    }

    response = generate_response(record)

    logger.info(
        "Candidate generated successfully."
    )

    return response


def main():

    sample = generate_candidate(

        domain="finance",

        language="en",

        difficulty="medium",

        skill="reasoning",

    )

    print()

    from pprint import pprint

    pprint(sample)


if __name__ == "__main__":
    main()