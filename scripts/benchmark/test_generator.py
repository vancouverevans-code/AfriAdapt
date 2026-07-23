"""
Smoke test for AfriBench generation.
Generates ONE benchmark candidate.
"""

import json
from pathlib import Path
import uuid

from scripts.benchmark.client import generate_candidate

OUTPUT = Path("datasets/benchmark/test_candidate.json")

candidate = generate_candidate(
    domain="finance",
    language="en",
    difficulty="easy",
    skill="reasoning"
)

record = {
    "id": f"AFB-{uuid.uuid4().hex[:8]}",
    "domain": "finance",
    "language": "en",
    "difficulty": "easy",
    "skill": "reasoning",
    **candidate,
    "metadata": {
        "version": "1.0",
        "reviewed": False,
        "pilot": True
    }
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=4, ensure_ascii=False)

print("\n✅ Test benchmark generated successfully.\n")
print(json.dumps(record, indent=2, ensure_ascii=False))