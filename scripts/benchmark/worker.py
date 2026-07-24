"""
AfriBench Benchmark Worker

Generates, validates and scores one benchmark example.
"""

import uuid

from scripts.benchmark.client import generate_candidate
from scripts.benchmark.benchmark_validator import validate_candidate
from scripts.benchmark.duplicate_checker import is_duplicate
from scripts.benchmark.quality import quality_score

from scripts.utils.logger import logger


def benchmark_worker(task, seen):
    """
    Process one benchmark task.

    Parameters
    ----------
    task : dict
        {
            domain,
            language,
            difficulty,
            skill
        }

    seen : set

    Returns
    -------
    tuple(status, record_or_error)
    """

    logger.info(
        "Generating | %s | %s | %s | %s",
        task["domain"],
        task["language"],
        task["difficulty"],
        task["skill"],
    )

    try:

        candidate = generate_candidate(
            domain=task["domain"],
            language=task["language"],
            difficulty=task["difficulty"],
            skill=task["skill"],
        )

    except Exception as e:

        return (
            "generation_error",
            str(e),
        )

    valid, errors = validate_candidate(candidate)

    if not valid:

        return (
            "validation_failed",
            errors,
        )

    if is_duplicate(
        candidate["instruction"],
        seen,
    ):

        return (
            "duplicate",
            None,
        )

    score = quality_score(candidate)

    record = {

        "id": f"AFB-{uuid.uuid4().hex[:8]}",

        "domain": task["domain"],

        "language": task["language"],

        "difficulty": task["difficulty"],

        "skill": task["skill"],

        "instruction":
            candidate["instruction"],

        "reference_answer":
            candidate["reference_answer"],

        "evaluation_criteria":
            candidate["evaluation_criteria"],

        "quality_score":
            score,

        "metadata": {

            "version": "1.1",

            "pilot": True,

            "reviewed": False,

        }

    }

    return (
        "success",
        record,
    )