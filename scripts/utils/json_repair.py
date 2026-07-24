"""
JSON repair utilities for AfriAdapt.
"""

import json


REQUIRED_FIELDS = {
    "instruction": "",
    "reference_answer": "",
    "evaluation_criteria": {},
}


def repair_json(data):
    """
    Ensure required fields always exist.
    """

    if data is None:
        data = {}

    if not isinstance(data, dict):
        return REQUIRED_FIELDS.copy()

    repaired = REQUIRED_FIELDS.copy()

    repaired.update(data)

    if repaired["evaluation_criteria"] is None:
        repaired["evaluation_criteria"] = {}

    return repaired


def safe_json_load(text):
    """
    Safely parse JSON.
    """

    try:
        return repair_json(json.loads(text))

    except Exception:
        return repair_json({})