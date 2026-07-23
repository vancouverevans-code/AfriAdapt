"""
AfriBench Benchmark Generator

Generates benchmark candidates using OpenRouter,
validates them, removes duplicates, assigns a quality
score, and saves them as JSONL.
"""

import json
import uuid
from pathlib import Path

from scripts.benchmark.client import generate_candidate
from scripts.benchmark.spec import (
    PILOT_DOMAINS as DOMAINS,
    PILOT_LANGUAGES as LANGUAGES,
    PILOT_DIFFICULTIES as DIFFICULTIES,
    PILOT_SKILLS as SKILLS,
)

from scripts.benchmark.benchmark_validator import validate_candidate
from scripts.benchmark.duplicate_checker import is_duplicate
from scripts.benchmark.quality import quality_score

OUTPUT = Path("datasets/benchmark/afribench_candidates.jsonl")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def main():

    seen = set()

    generated = 0
    skipped_duplicates = 0
    skipped_validation = 0

    with open(OUTPUT, "w", encoding="utf-8") as outfile:

        for domain in DOMAINS:
            for language in LANGUAGES:
                for difficulty in DIFFICULTIES:
                    for skill in SKILLS:

                        print("=" * 60)
                        print(f"Domain      : {domain}")
                        print(f"Language    : {language}")
                        print(f"Difficulty  : {difficulty}")
                        print(f"Skill       : {skill}")

                        try:

                            candidate = generate_candidate(
                                domain=domain,
                                language=language,
                                difficulty=difficulty,
                                skill=skill,
                            )

                        except Exception as e:

                            print(f"Generation failed: {e}")
                            continue

                        # ----------------------------
                        # Validation
                        # ----------------------------

                        valid, errors = validate_candidate(candidate)

                        if not valid:

                            print("Validation failed.")

                            for err in errors:
                                print(f"  - {err}")

                            skipped_validation += 1
                            continue

                        # ----------------------------
                        # Duplicate Detection
                        # ----------------------------

                        if is_duplicate(
                            candidate["instruction"],
                            seen,
                        ):

                            print("Duplicate skipped.")

                            skipped_duplicates += 1
                            continue

                        # ----------------------------
                        # Quality Score
                        # ----------------------------

                        score = quality_score(candidate)

                        # ----------------------------
                        # Final Record
                        # ----------------------------

                        record = {

                            "id": f"AFB-{uuid.uuid4().hex[:8]}",

                            "domain": domain,

                            "language": language,

                            "difficulty": difficulty,

                            "skill": skill,

                            "instruction": candidate["instruction"],

                            "reference_answer": candidate["reference_answer"],

                            "evaluation_criteria":
                                candidate["evaluation_criteria"],

                            "quality_score": score,

                            "metadata": {

                                "version": "1.0",

                                "reviewed": False,

                                "pilot": True,

                            }
                        }

                        outfile.write(
                            json.dumps(
                                record,
                                ensure_ascii=False,
                            ) + "\n"
                        )

                        generated += 1

                        print(f"✓ Saved ({score}/10)")

    print("\n" + "=" * 60)
    print("AfriBench Generation Complete")
    print("=" * 60)

    print(f"Generated            : {generated}")
    print(f"Validation Failed    : {skipped_validation}")
    print(f"Duplicates Skipped   : {skipped_duplicates}")
    print(f"Output File          : {OUTPUT}")


if __name__ == "__main__":
    main()