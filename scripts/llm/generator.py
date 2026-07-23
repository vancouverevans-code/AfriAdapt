"""
Generate responses using OpenRouter.
"""

import json

from scripts.llm.client import client
from scripts.llm.config import (
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

from scripts.llm.prompts import get_system_prompt


def generate_response(record):

    response = client.chat.completions.create(

        model=MODEL,

        temperature=TEMPERATURE,

        max_tokens=MAX_TOKENS,

        response_format={
            "type": "json_object"
        },

        messages=[
            {
                "role": "system",
                "content": get_system_prompt(
                    record["metadata"]["domain"]
                )
            },

            {
                "role": "user",
                "content": record["instruction"]
            }
        ]
    )

    content = response.choices[0].message.content

    return json.loads(content)