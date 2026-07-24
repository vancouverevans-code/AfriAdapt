"""
Benchmark Repair Agent

Attempts to repair malformed benchmark JSON
instead of discarding it.
"""

import json

from scripts.llm.client import client
from scripts.llm.config import MODEL

from scripts.utils.logger import logger


SYSTEM_PROMPT = """
You repair benchmark JSON.

Your job is NOT to rewrite the benchmark.

Instead:

• Preserve the meaning.

• Preserve the instruction.

• Preserve the reference answer.

• Add missing fields.

• Fix malformed JSON.

Return ONLY valid JSON.

Required schema:

{
    "instruction": "...",

    "reference_answer": "...",

    "evaluation_criteria": {

        "accuracy":"...",

        "local_context":"...",

        "clarity":"...",

        "completeness":"...",

        "safe_response":"..."

    }

}
"""


def repair_candidate(candidate):

    logger.info("Repairing invalid benchmark...")

    try:

        response = client.chat.completions.create(

            model=MODEL,

            temperature=0,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },

                {
                    "role": "user",
                    "content": json.dumps(
                        candidate,
                        ensure_ascii=False,
                        indent=2,
                    ),
                },

            ],

        )

        repaired = json.loads(
            response.choices[0].message.content
        )

        logger.info("Repair successful.")

        return repaired

    except Exception:

        logger.exception(
            "Repair failed."
        )

        return None