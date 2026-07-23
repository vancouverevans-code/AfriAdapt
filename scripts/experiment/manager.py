"""
Experiment Manager
"""

import json
from pathlib import Path
from datetime import datetime


class ExperimentManager:

    def __init__(self):

        self.base = Path("outputs/experiments")

        self.base.mkdir(
            parents=True,
            exist_ok=True
        )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.path = self.base / f"EXP_{timestamp}"

        self.path.mkdir()

    def save_json(
        self,
        filename,
        data
    ):

        with open(
            self.path / filename,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    def save_text(
        self,
        filename,
        text
    ):

        with open(
            self.path / filename,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

    def location(self):

        return self.path