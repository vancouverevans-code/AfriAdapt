"""
Simple duplicate detector.
"""


def is_duplicate(instruction, seen):

    normalized = instruction.lower().strip()

    if normalized in seen:
        return True

    seen.add(normalized)

    return False