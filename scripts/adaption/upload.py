"""
Upload AfriAdapt dataset to Adaption.
"""

from pathlib import Path

from adaption import Adaption

client = Adaption()

DATASET = Path("datasets/generated/afriadapt_train.jsonl")

print("=" * 60)
print("Uploading Dataset")
print("=" * 60)

result = client.datasets.upload_file(str(DATASET))

print("\nUpload started!")
print(f"Dataset ID: {result.dataset_id}")