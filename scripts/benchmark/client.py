"""
Benchmark generation client.
"""

import json

from scripts.llm.client import client
from scripts.llm.config import (
    MODEL,
    TEMPERATURE,
)

from scripts.benchmark.prompts import build_prompt


def generate_candidate(
    domain,
    language,
    difficulty,
    skill,
):

    response = client.chat.completions.create(

        model=MODEL,

        temperature=TEMPERATURE,

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "user",
                "content": build_prompt(
                    domain,
                    language,
                    difficulty,
                    skill,
                ),
            }
        ],
    )

    return json.loads(
        response.choices[0].message.content
    )