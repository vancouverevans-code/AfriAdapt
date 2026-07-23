"""
AfriAdapt Dataset Schema
"""

from dataclasses import dataclass, asdict


@dataclass
class DatasetSample:
    id: str
    language: str
    domain: str
    subcategory: str
    difficulty: str
    reasoning_type: str
    instruction: str
    context: str
    response: str
    source: str
    reviewed: bool = False
    quality_score: float | None = None

    def to_dict(self):
        return asdict(self)