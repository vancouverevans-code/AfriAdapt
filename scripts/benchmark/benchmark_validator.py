"""
AfriBench Validator

Ensures generated benchmark items satisfy
the AfriBench schema and quality rules.
"""

REQUIRED_FIELDS = [
    "instruction",
    "reference_answer",
    "evaluation_criteria",
]


def validate_candidate(candidate):

    errors = []

    for field in REQUIRED_FIELDS:
        if field not in candidate:
            errors.append(f"Missing field: {field}")

    instruction = candidate.get("instruction", "").strip()
    answer = candidate.get("reference_answer", "").strip()

    if len(instruction) < 25:
        errors.append("Instruction too short")

    if len(answer) < 80:
        errors.append("Reference answer too short")

    criteria = candidate.get("evaluation_criteria", {})

    required_checks = [
        "accuracy",
        "local_context",
        "clarity",
        "completeness",
        "safe_response",
    ]

    for check in required_checks:
        if check not in criteria:
            errors.append(f"Missing evaluation criterion: {check}")

    return len(errors) == 0, errors