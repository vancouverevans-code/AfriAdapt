"""
Simple benchmark quality scoring.
"""


def quality_score(candidate):

    score = 0

    if len(candidate["instruction"]) > 60:
        score += 2

    if len(candidate["reference_answer"]) > 150:
        score += 2

    if candidate["evaluation_criteria"].get("local_context"):
        score += 2

    if candidate["evaluation_criteria"].get("accuracy"):
        score += 2

    if candidate["evaluation_criteria"].get("safe_response"):
        score += 2

    return score