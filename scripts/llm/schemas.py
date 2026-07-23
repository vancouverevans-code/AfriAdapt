from pydantic import BaseModel, Field
from typing import Optional


class Metadata(BaseModel):
    domain: str
    language: str
    difficulty: str
    reasoning_type: str
    generator: str
    created_at: str


class DatasetRecord(BaseModel):
    id: str
    system: str
    instruction: str
    input: str = ""
    output: str = ""
    quality_score: Optional[float] = None
    status: str = "pending"
    metadata: Metadata