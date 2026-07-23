"""
Experiment utilities.
"""

import uuid

from datetime import datetime


def new_experiment():

    return {

        "id":
            f"EXP-{uuid.uuid4().hex[:8]}",

        "timestamp":
            datetime.utcnow().isoformat(),

        "status":
            "running",

    }