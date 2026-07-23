"""
Wait until dataset ingestion completes.
"""

import time

from adaption import Adaption

client = Adaption()

DATASET_ID = input("Dataset ID: ")

print("\nWaiting for ingestion...\n")

while True:

    status = client.datasets.get_status(DATASET_ID)

    print(
        f"Status: {status.status}"
    )

    if status.row_count is not None:
        print("\nDataset ready!")
        print(f"Rows: {status.row_count}")
        break

    time.sleep(5)