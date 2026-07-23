"""
AfriAdapt Evaluator

Runs the complete evaluation pipeline.
"""

import json

from scripts.evaluation.judge import judge_response
from scripts.evaluation.metrics import aggregate
from scripts.evaluation.report import save_report

from scripts.llm.generator import generate_response

from scripts.utils.paths import BENCHMARK_OUTPUT


def load_benchmark():

    with open(
        BENCHMARK_OUTPUT,
        "r",
        encoding="utf-8",
    ) as file:

        return [

            json.loads(line)

            for line in file

        ]


def main():

    benchmark = load_benchmark()

    results = []

    for sample in benchmark:

        print(sample["instruction"][:60])

        generated = generate_response(sample)

        judged = judge_response(

            sample,

            generated["answer"]

            if "answer" in generated

            else str(generated),

        )

        results.append(judged)

    metrics = aggregate(results)

    save_report(metrics)

    print()

    print(metrics)


if __name__ == "__main__":
    main()