"""
AfriBench Benchmark Generator

Generates benchmark candidates, validates them,
removes duplicates, scores quality, and exports
them as JSONL.
"""

import json
import uuid
from typing import Dict

from scripts.benchmark.client import generate_candidate
from scripts.benchmark.spec import (
    PILOT_DOMAINS,
    PILOT_LANGUAGES,
    PILOT_DIFFICULTIES,
    PILOT_SKILLS,
)

from scripts.benchmark.benchmark_validator import validate_candidate
from scripts.benchmark.duplicate_checker import is_duplicate
from scripts.benchmark.quality import quality_score

from scripts.utils.paths import BENCHMARK_OUTPUT
from scripts.utils.logger import logger
from scripts.utils.experiment import new_experiment

OUTPUT = BENCHMARK_OUTPUT


def save_record(record: Dict, outfile):

    outfile.write(
        json.dumps(
            record,
            ensure_ascii=False,
        )
        + "\n"
    )


def main():

    experiment = new_experiment()

    logger.info(
        "Benchmark experiment started: %s",
        experiment["id"],
    )

    print("=" * 70)
    print("AfriBench Benchmark Generator")
    print("=" * 70)

    seen = set()

    generated = 0
    validation_failed = 0
    duplicates = 0
    generation_errors = 0

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as outfile:

        for domain in PILOT_DOMAINS:

            for language in PILOT_LANGUAGES:

                for difficulty in PILOT_DIFFICULTIES:

                    for skill in PILOT_SKILLS:

                        print("\n" + "-" * 60)

                        print(f"Domain      : {domain}")
                        print(f"Language    : {language}")
                        print(f"Difficulty  : {difficulty}")
                        print(f"Skill       : {skill}")

                        logger.info(
                            "Generating | %s | %s | %s | %s",
                            domain,
                            language,
                            difficulty,
                            skill,
                        )

                        try:

                            candidate = generate_candidate(
                                domain=domain,
                                language=language,
                                difficulty=difficulty,
                                skill=skill,
                            )

                        except Exception as e:

                            generation_errors += 1

                            logger.exception(
                                "Generation failed."
                            )

                            print(f"\nGeneration failed:\n{e}")

                            continue

                        valid, errors = validate_candidate(candidate)

                        if not valid:

                            validation_failed += 1

                            logger.warning(
                                "Validation failed."
                            )

                            print("\nValidation failed")

                            for err in errors:

                                print(f" • {err}")

                            continue

                        if is_duplicate(
                            candidate["instruction"],
                            seen,
                        ):

                            duplicates += 1

                            logger.info(
                                "Duplicate skipped."
                            )

                            print("Duplicate skipped")

                            continue

                        score = quality_score(candidate)

                        record = {

                            "id":
                                f"AFB-{uuid.uuid4().hex[:8]}",

                            "domain":
                                domain,

                            "language":
                                language,

                            "difficulty":
                                difficulty,

                            "skill":
                                skill,

                            "instruction":
                                candidate["instruction"],

                            "reference_answer":
                                candidate["reference_answer"],

                            "evaluation_criteria":
                                candidate["evaluation_criteria"],

                            "quality_score":
                                score,

                            "metadata": {

                                "experiment":
                                    experiment["id"],

                                "version":
                                    "1.0",

                                "pilot":
                                    True,

                                "reviewed":
                                    False,

                            }

                        }

                        save_record(
                            record,
                            outfile,
                        )

                        generated += 1

                        logger.info(
                            "Saved benchmark case."
                        )

                        print(
                            f"Saved (Quality {score}/10)"
                        )

    print("\n" + "=" * 70)

    print("AfriBench Generation Complete")

    print("=" * 70)

    print(f"Generated            : {generated}")

    print(f"Validation Failed    : {validation_failed}")

    print(f"Duplicates Removed   : {duplicates}")

    print(f"Generation Errors    : {generation_errors}")

    print(f"Saved To             : {OUTPUT}")

    logger.info(
        "Benchmark experiment finished."
    )


if __name__ == "__main__":
    main()