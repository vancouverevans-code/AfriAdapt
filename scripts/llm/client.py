"""
OpenRouter client for AfriAdapt.
"""

from openai import OpenAI

from scripts.llm.config import (
    OPENROUTER_API_KEY,
    BASE_URL,
)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
)