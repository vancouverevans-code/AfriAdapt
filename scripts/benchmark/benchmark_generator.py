"""
AfriBench Benchmark Generator

Production benchmark generation pipeline.

Features
--------
✓ Parallel execution
✓ Automatic validation
✓ Duplicate removal
✓ Quality scoring
✓ Checkpoint & Resume
✓ Experiment tracking
"""

import json
from pathlib import Path

from scripts.benchmark.parallel import run_parallel
from scripts.benchmark.worker import benchmark_worker

from scripts.benchmark.spec import (
    PILOT_DOMAINS,
    PILOT_LANGUAGES,
    PILOT_DIFFICULTIES,
    PILOT_SKILLS,
)

from scripts.benchmark.checkpoint import (
    save_checkpoint,
    load_checkpoint,
    clear_checkpoint,
)

from scripts.utils.logger import logger

from scripts.utils.experiment import (
    start_experiment,
    finish_experiment,
)

from scripts.utils.paths import BENCHMARK_OUTPUT


OUTPUT = Path(BENCHMARK_OUTPUT)


# ---------------------------------------------------------
# Build Tasks
# ---------------------------------------------------------

def build_tasks():
    """
    Build every benchmark combination.
    """

    tasks = []

    for domain in PILOT_DOMAINS:

        for language in PILOT_LANGUAGES:

            for difficulty in PILOT_DIFFICULTIES:

                for skill in PILOT_SKILLS:

                    tasks.append({

                        "domain": domain,

                        "language": language,

                        "difficulty": difficulty,

                        "skill": skill,

                    })

    return tasks


# ---------------------------------------------------------
# Worker Wrapper
# ---------------------------------------------------------

seen = set()


def worker(task):

    return benchmark_worker(
        task,
        seen,
    )


# ---------------------------------------------------------
# Save JSONL
# ---------------------------------------------------------

def save_records(records):

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as outfile:

        for record in records:

            outfile.write(

                json.dumps(
                    record,
                    ensure_ascii=False,
                )

                + "\n"

            )


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    logger.info("=" * 70)
    logger.info("AfriBench Benchmark Generator")
    logger.info("=" * 70)

    start_experiment("Benchmark")

    state = load_checkpoint()

    completed = state["completed"]

    generated = state["generated"]

    duplicates = state["duplicates"]

    validation_failed = state["validation_failed"]

    generation_errors = state["generation_errors"]

    tasks = build_tasks()

    logger.info(
        "Total benchmark tasks : %s",
        len(tasks),
    )

    if completed > 0:

        logger.info(
            "Skipping first %s completed tasks.",
            completed,
        )

    tasks = tasks[completed:]

    records = []

    results = run_parallel(
        tasks,
        worker,
    )

    for status, payload in results:

        completed += 1

        if status == "success":

            generated += 1

            records.append(payload)

        elif status == "duplicate":

            duplicates += 1

        elif status == "validation_failed":

            validation_failed += 1

            logger.warning(payload)

        elif status == "generation_error":

            generation_errors += 1

            logger.error(payload)

        # ----------------------------------
        # Save every 10 completed tasks
        # ----------------------------------

        if completed % 10 == 0:

            save_checkpoint(

                completed=completed,

                generated=generated,

                duplicates=duplicates,

                validation_failed=validation_failed,

                generation_errors=generation_errors,

            )

    save_records(records)

    clear_checkpoint()

    logger.info("")
    logger.info("=" * 70)
    logger.info("AfriBench Generation Complete")
    logger.info("=" * 70)

    logger.info(
        "Generated            : %s",
        generated,
    )

    logger.info(
        "Duplicates           : %s",
        duplicates,
    )

    logger.info(
        "Validation Failed    : %s",
        validation_failed,
    )

    logger.info(
        "Generation Errors    : %s",
        generation_errors,
    )

    logger.info(
        "Completed Tasks      : %s",
        completed,
    )

    logger.info(
        "Saved To             : %s",
        OUTPUT,
    )

    finish_experiment()


if __name__ == "__main__":

    main()