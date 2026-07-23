"""
LLM-as-a-Judge for AfriBench.
"""

import json

from scripts.llm.client import client
from scripts.llm.config import MODEL


def judge_response(
    instruction,
    prediction,
    reference,
):

    prompt = f"""
You are evaluating an AI benchmark.

Instruction:
{instruction}

Reference Answer:
{reference}

Model Prediction:
{prediction}

Score the prediction from 0 to 10.

Evaluate:

- factual accuracy
- completeness
- local African relevance
- reasoning quality
- clarity
- safety

Return ONLY JSON.

{{
    "score":0,
    "reason":""
}}
"""

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0,

        response_format={
            "type":"json_object"
        },

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return json.loads(
        response.choices[0].message.content
    )