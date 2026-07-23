"""
AfriAdapt Universal Dataset Generator

Generates structured instruction records from all supported domains,
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

# Load project configuration
config = load_config()

# Output directory
OUTPUT_DIR = Path("datasets/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "afriadapt_train.jsonl"


def generate_dataset():
    """
    Generate instruction records across all configured domains.
    """
    dataset = []

    samples_per_domain = config["generation"]["train_per_domain"]

    for domain in config["domains"]:

        print(f"Generating {domain}...")

        for _ in range(samples_per_domain):

            # Build a prompt
            prompt = build_prompt(domain)

            # Convert it into a training record
            record = build_record(prompt)

            dataset.append(record)

    return dataset


def export_jsonl(dataset, output_file):
    """
    Export dataset to JSONL format.
    """
    with open(output_file, "w", encoding="utf-8") as file:
        for sample in dataset:
            file.write(json.dumps(sample, ensure_ascii=False) + "\n")

    print("\nDataset successfully exported!")
    print(f"Saved {len(dataset)} samples")
    print(f"Location: {output_file}")


def main():

    print("=" * 60)
    print("AfriAdapt Universal Dataset Generator")
    print("=" * 60)

    # Generate records
    dataset = generate_dataset()

    print(f"\nGenerated {len(dataset)} records.")

    # Remove duplicate instructions
    dataset = remove_duplicate_instructions(dataset)

    print(f"Remaining after deduplication: {len(dataset)} records.")

    # Display statistics
    summarize_dataset(dataset)

    # Export dataset
    export_jsonl(dataset, OUTPUT_FILE)

    print("\n✅ Dataset generation completed successfully!")


if __name__ == "__main__":
    main()