"""
AfriAdapt Dataset Validator
"""

from collections import Counter


def remove_duplicate_instructions(samples):
    """
    Remove samples with duplicate instructions.
    """
    seen = set()
    unique = []

    for sample in samples:
        instruction = sample["instruction"]

        if instruction not in seen:
            seen.add(instruction)
            unique.append(sample)

    return unique


def summarize_dataset(samples):
    """
    Print dataset statistics.
    """
    languages = Counter(sample["language"] for sample in samples)
    difficulties = Counter(sample["difficulty"] for sample in samples)
    reasoning = Counter(sample["reasoning_type"] for sample in samples)

    print("\nDataset Summary")
    print("-" * 30)

    print("Languages")
    print(dict(languages))

    print("\nDifficulty")
    print(dict(difficulties))

    print("\nReasoning")
    print(dict(reasoning))