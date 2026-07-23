"""
AfriAdapt Record Builder

Converts prompts into complete instruction records.
"""

from datetime import datetime


def build_record(prompt):
    """
    Convert a generated prompt into a training record.
    """

    return {
        "id": prompt["id"],
        "instruction": prompt["instruction"],
        "context": "",
        "response": "",
        "domain": prompt["domain"],
        "language": prompt["language"],
        "difficulty": prompt["difficulty"],
        "reasoning_type": prompt["reasoning_type"],
        "metadata": {
            "created_at": datetime.utcnow().isoformat(),
            "generator": "AfriAdapt v0.1",
            "status": "pending_response",
            "quality_score": None,
        },
    }