"""
AfriAdapt - Adaption Connection Test
"""

import os

from dotenv import load_dotenv
from adaption import Adaption

load_dotenv()

client = Adaption()

print("=" * 60)
print("AfriAdapt → Adaption")
print("=" * 60)

try:
    page = client.datasets.list()

    print("\n✅ Authentication successful!")

    print(f"\nDatasets found: {len(page.datasets)}")

    if page.datasets:
        print("\nExisting datasets:\n")

        for ds in page.datasets:
            print(f"{ds.dataset_id} | {ds.name}")

    else:
        print("\nNo datasets found.")

except Exception as e:
    print("\nConnection failed")
    print(type(e).__name__)
    print(e)