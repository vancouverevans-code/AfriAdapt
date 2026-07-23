"""
Generate experiment report.
"""

import json
from pathlib import Path

OUTPUT = Path(
    "reports/evaluation_report.json"
)


def save_report(report):

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False,
        )

    print(
        f"\nSaved report to {OUTPUT}"
    )