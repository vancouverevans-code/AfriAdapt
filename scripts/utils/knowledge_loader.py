"""
AfriAdapt Knowledge Loader

Loads all domain knowledge from JSON files.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
RAW_DATA = ROOT / "datasets" / "raw"


def load_json(filename):
    """Load a JSON list from datasets/raw."""
    path = RAW_DATA / filename
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_knowledge():
    """Load all knowledge sources."""
    return {
        "finance": load_json("finance.json"),
        "agriculture": load_json("agriculture.json"),
        "languages": load_json("languages.json"),
        "personas": load_json("personas.json"),
    }


if __name__ == "__main__":
    data = load_knowledge()

    for name, values in data.items():
        print(f"{name}: {len(values)} entries")