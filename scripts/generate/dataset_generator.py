"""
AfriAdapt Universal Dataset Generator

Generates structured instruction records from all configured domains,
validates them, removes duplicates, and exports them to JSONL.
"""

import json
from pathlib import Path

from scripts.generate.prompt_builder import build_prompt
from scripts.generate.record_builder import build_record
from scripts.generate.validator import (
    remove_duplicate_instructions,
    summarize_dataset,
)
from scripts.utils.config import load_config

# ----------------------------------------------------
# Load configuration
# ----------------------------------------------------

config = load_config()

OUTPUT_DIR = Path("datasets/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "afriadapt_train.jsonl"


def get_domains():
    """
    Return configured domains or sensible defaults.
    """

    return config.get(
        "domains",
        [
            "finance",
            "agriculture",
            "language",
            "communications",
        ],
    )


def get_samples_per_domain():
    """
    Determine how many samples to generate
    for each domain.

    Supports both:

    generation:
        train_per_domain: 100

    and

    generation:
        dataset_size: 2000
    """

    generation_cfg = config.get("generation", {})

    # Preferred setting
    if "train_per_domain" in generation_cfg:
        return generation_cfg["train_per_domain"]

    dataset_size = generation_cfg.get("dataset_size", 100)

    domains = get_domains()

    return max(
        1,
        dataset_size // len(domains),
    )


def generate_dataset():
    """
    Generate the complete dataset.
    """

    dataset = []

    domains = get_domains()

    samples_per_domain = get_samples_per_domain()

    print(f"\nDomains: {domains}")
    print(f"Samples per domain: {samples_per_domain}\n")

    for domain in domains:

        print(f"Generating {domain}...")

        for _ in range(samples_per_domain):

            prompt = build_prompt(domain)

            record = build_record(prompt)

            dataset.append(record)

    return dataset


def export_jsonl(dataset, output_file):
    """
    Export dataset to JSONL.
    """

    with open(output_file, "w", encoding="utf-8") as file:

        for sample in dataset:

            file.write(
                json.dumps(
                    sample,
                    ensure_ascii=False,
                )
                + "\n"
            )

    print("\nDataset exported successfully.")

    print(f"Samples : {len(dataset)}")

    print(f"Location: {output_file}")


def main():

    print("=" * 60)
    print("AfriAdapt Universal Dataset Generator")
    print("=" * 60)

    dataset = generate_dataset()

    print(f"\nGenerated {len(dataset)} records.")

    dataset = remove_duplicate_instructions(
        dataset
    )

    print(
        f"Remaining after deduplication: {len(dataset)}"
    )

    summarize_dataset(dataset)

    export_jsonl(
        dataset,
        OUTPUT_FILE,
    )

    print("\nDataset generation completed successfully.")


if __name__ == "__main__":
    main()