"""
LLM configuration for AfriAdapt.
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found in .env")

BASE_URL = "https://openrouter.ai/api/v1"

MODEL = "qwen/qwen-2.5-72b-instruct"

TEMPERATURE = 0.3

MAX_TOKENS = 512