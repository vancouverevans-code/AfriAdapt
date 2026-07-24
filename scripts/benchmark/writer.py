"""
AfriBench JSONL Writer

Handles streaming benchmark writes, loading existing
records, and resetting output files.
"""

import json
from pathlib import Path

from scripts.utils.logger import logger


class BenchmarkWriter:

    def __init__(self, output_path):

        self.output = Path(output_path)

        self.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def append(self, record):
        """
        Append a single benchmark record.
        """

        with open(
            self.output,
            "a",
            encoding="utf-8",
        ) as file:

            file.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )

    def load_existing(self):
        """
        Load all previously generated benchmark records.

        Returns
        -------
        list
        """

        if not self.output.exists():

            return []

        records = []

        with open(
            self.output,
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                try:

                    records.append(
                        json.loads(line)
                    )

                except json.JSONDecodeError:

                    logger.warning(
                        "Skipping corrupted benchmark record."
                    )

        logger.info(
            "Loaded %s existing benchmark records.",
            len(records),
        )

        return records

    def reset(self):
        """
        Remove the benchmark file so a fresh run
        starts with an empty dataset.
        """

        if self.output.exists():

            self.output.unlink()

            logger.info(
                "Existing benchmark file removed."
            )

    def exists(self):
        """
        Check whether the output file exists.
        """

        return self.output.exists()

    def count(self):
        """
        Count stored benchmark records.
        """

        return len(self.load_existing())