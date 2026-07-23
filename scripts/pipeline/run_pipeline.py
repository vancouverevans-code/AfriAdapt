"""
AfriAdapt Pipeline Runner

Runs the complete AfriAdapt research workflow.

Pipeline Stages:
1. Preflight Checks
2. Environment Check
3. Dataset Generation
4. Benchmark Generation
5. Evaluation
"""

import time

from scripts.utils.preflight import main as preflight
from scripts.utils.check_environment import main as check_environment

from scripts.generate.dataset_generator import (
    main as generate_dataset,
)

from scripts.benchmark.benchmark_generator import (
    main as generate_benchmark,
)

from scripts.evaluation.evaluator import (
    main as evaluate,
)

from scripts.utils.logger import logger


def run_stage(name, func):
    """
    Run one pipeline stage while measuring runtime.
    """

    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    logger.info(f"Starting stage: {name}")

    start = time.perf_counter()

    try:

        func()

    except Exception as e:

        logger.exception(f"{name} failed")

        raise RuntimeError(
            f"\n{name} failed.\n{e}"
        ) from e

    elapsed = round(
        time.perf_counter() - start,
        2,
    )

    logger.info(
        f"{name} completed in {elapsed} seconds"
    )

    print(f"\n{name} completed in {elapsed} seconds")


def main():

    overall = time.perf_counter()

    print("=" * 70)
    print("AfriAdapt Research Pipeline")
    print("=" * 70)

    stages = [

        ("Preflight Checks", preflight),

        ("Environment Check", check_environment),

        ("Dataset Generation", generate_dataset),

        ("Benchmark Generation", generate_benchmark),

        ("Evaluation", evaluate),

    ]

    for stage_name, stage_function in stages:

        run_stage(
            stage_name,
            stage_function,
        )

    total = round(
        time.perf_counter() - overall,
        2,
    )

    print("\n" + "=" * 70)
    print("AfriAdapt Pipeline Completed Successfully")
    print("=" * 70)
    print(f"Total Runtime : {total} seconds")

    logger.info(
        f"Pipeline completed successfully in {total} seconds."
    )


if __name__ == "__main__":
    main()