"""
AfriAdapt Dataset Generation Pipeline

Loads instruction records, generates responses,
validates them, and exports a completed dataset.
"""

import json
from pathlib import Path

from scripts.llm.generator import generate_response
from scripts.llm.validator import validate_response

INPUT_FILE = Path("datasets/generated/afriadapt_train.jsonl")
OUTPUT_FILE = Path("datasets/generated/training.jsonl")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_records():

    records = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:

        for line in file:

            records.append(json.loads(line))

    return records


def save_records(records):

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        for record in records:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False
                ) + "\n"
            )


def process_record(record):

    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):

        result = generate_response(record)

        output = result["output"]

        if validate_response(output):

            record["output"] = output
            record["status"] = "generated"
            record["quality_score"] = None

            return record

        print(
            f"Retry {attempt+1}/3 : {record['id']}"
        )

    record["status"] = "failed"

    return record


def main():

    records = load_records()

    completed = []

    total = len(records)

    print(f"\nLoaded {total} records\n")

    for index, record in enumerate(records):

        print(
            f"[{index+1}/{total}] {record['metadata']['domain']}"
        )

        completed.append(
            process_record(record)
        )

    save_records(completed)

    print("\nDone!")

    print(
        f"Saved to {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()