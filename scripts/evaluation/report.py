"""
AfriAdapt Report Generator
"""

import json
from datetime import datetime

from scripts.utils.paths import REPORTS


def save_report(metrics):

    timestamp = datetime.utcnow().isoformat()

    json_file = REPORTS / "evaluation.json"

    md_file = REPORTS / "evaluation.md"

    report = {

        "generated_at": timestamp,

        "metrics": metrics,

    }

    with open(json_file, "w", encoding="utf-8") as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False,
        )

    with open(md_file, "w", encoding="utf-8") as f:

        f.write("# AfriAdapt Evaluation Report\n\n")

        f.write(f"Generated: {timestamp}\n\n")

        for key, value in metrics.items():

            f.write(f"- **{key}**: {value}\n")