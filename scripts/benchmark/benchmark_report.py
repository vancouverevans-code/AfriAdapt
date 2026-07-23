"""
Generate benchmark statistics.
"""

import json

from scripts.benchmark.scorer import score_prediction
from scripts.utils.paths import OUTPUTS

INPUT = OUTPUTS / "benchmark_predictions.jsonl"


def main():

    scores = []

    with open(INPUT, "r", encoding="utf-8") as f:

        for line in f:

            record = json.loads(line)

            score = score_prediction(

                record["prediction"],

                record["reference_answer"]

            )

            scores.append(score)

    average = sum(scores) / len(scores)

    print("\nAfriBench Report")

    print("-" * 40)

    print(f"Examples : {len(scores)}")
    print(f"Average  : {average:.2f}")
    print(f"Highest  : {max(scores):.2f}")
    print(f"Lowest   : {min(scores):.2f}")


if __name__ == "__main__":
    main()