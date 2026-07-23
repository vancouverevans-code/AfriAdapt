"""
Run a model against AfriBench.
"""

import json

from scripts.llm.generator import generate_response

from scripts.utils.paths import (
    BENCHMARK_FINAL,
    OUTPUTS,
)

BENCHMARK = BENCHMARK_FINAL

OUTPUT = OUTPUTS / "benchmark_predictions.jsonl"


def load_benchmark():

    benchmark = []

    with open(BENCHMARK, "r", encoding="utf-8") as f:

        for line in f:

            benchmark.append(
                json.loads(line)
            )

    return benchmark


def main():

    benchmark = load_benchmark()

    predictions = []

    print(f"Loaded {len(benchmark)} benchmark cases")

    for record in benchmark:

        try:

            result = generate_response({

                "instruction":
                    record["instruction"]

            })

            prediction = result["output"]

        except Exception:

            prediction = ""

        predictions.append({

            "id":
                record["id"],

            "prediction":
                prediction,

            "reference_answer":
                record["reference_answer"],

            "evaluation_criteria":
                record["evaluation_criteria"]

        })

    with open(OUTPUT, "w", encoding="utf-8") as f:

        for record in predictions:

            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print(f"Saved predictions to {OUTPUT}")


if __name__ == "__main__":
    main()