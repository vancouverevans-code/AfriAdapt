"""
Benchmark checkpoint manager.

Handles automatic saving and resuming of benchmark generation.
"""

import json
from pathlib import Path

from scripts.utils.logger import logger


CHECKPOINT = Path(
    "outputs/checkpoints/benchmark_checkpoint.json"
)

CHECKPOINT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


def save_checkpoint(
    completed,
    generated,
    duplicates,
    validation_failed,
    generation_errors,
):
    """
    Save pipeline state.
    """

    payload = {

        "completed": completed,

        "generated": generated,

        "duplicates": duplicates,

        "validation_failed": validation_failed,

        "generation_errors": generation_errors,

    }

    with open(
        CHECKPOINT,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            payload,
            file,
            indent=2,
        )

    logger.info(
        "Checkpoint saved (%s completed).",
        completed,
    )


def load_checkpoint():
    """
    Load checkpoint if present.
    """

    if not CHECKPOINT.exists():

        return {

            "completed": 0,

            "generated": 0,

            "duplicates": 0,

            "validation_failed": 0,

            "generation_errors": 0,

        }

    with open(
        CHECKPOINT,
        "r",
        encoding="utf-8",
    ) as file:

        state = json.load(file)

    logger.info(
        "Resuming from checkpoint (%s completed).",
        state["completed"],
    )

    return state


def clear_checkpoint():

    if CHECKPOINT.exists():

        CHECKPOINT.unlink()

        logger.info("Checkpoint cleared.")