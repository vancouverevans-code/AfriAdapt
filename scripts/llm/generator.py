"""
LLM Response Generator

Central interface for all LLM calls in AfriAdapt.

Features
--------
- Automatic retries
- Safe JSON parsing
- Response validation
- Token usage tracking
- Latency tracking
- Structured logging
"""

import time
from typing import Dict, Optional

from scripts.llm.client import client
from scripts.llm.config import (
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

from scripts.llm.prompts import get_system_prompt
from scripts.utils.json_repair import safe_json_load
from scripts.utils.logger import logger


MAX_RETRIES = 3
RETRY_DELAY = 2


def generate_response(
    record: Dict,
    *,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> Dict:
    """
    Generate a structured response from the configured LLM.
    """

    if "instruction" not in record:
        raise ValueError("Record missing 'instruction'.")

    metadata = record.get("metadata", {})

    domain = metadata.get(
        "domain",
        record.get("domain", "general"),
    )

    logger.info(
        "Generating response | domain=%s",
        domain,
    )

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        start = time.perf_counter()

        try:

            response = client.chat.completions.create(

                model=model or MODEL,

                temperature=(
                    temperature
                    if temperature is not None
                    else TEMPERATURE
                ),

                max_tokens=(
                    max_tokens
                    if max_tokens is not None
                    else MAX_TOKENS
                ),

                response_format={
                    "type": "json_object"
                },

                messages=[

                    {
                        "role": "system",
                        "content": get_system_prompt(domain),
                    },

                    {
                        "role": "user",
                        "content": record["instruction"],
                    },

                ],
            )

            elapsed = round(
                time.perf_counter() - start,
                2,
            )

            logger.info(
                "Completed in %.2fs",
                elapsed,
            )

            # -------------------------
            # Validate response object
            # -------------------------

            if response is None:
                raise RuntimeError("Response is None.")

            if getattr(response, "choices", None) is None:
                raise RuntimeError("choices is None.")

            if len(response.choices) == 0:
                raise RuntimeError("No choices returned.")

            message = response.choices[0].message

            if message is None:
                raise RuntimeError("Message is None.")

            content = message.content

            if content is None:
                raise RuntimeError("Model returned empty content.")

            usage = getattr(response, "usage", None)

            result = safe_json_load(content)

            result["_metadata"] = {

                "model":
                    model or MODEL,

                "temperature":
                    temperature
                    if temperature is not None
                    else TEMPERATURE,

                "latency_seconds":
                    elapsed,

                "token_usage":
                    None if usage is None else {

                        "prompt_tokens":
                            getattr(
                                usage,
                                "prompt_tokens",
                                None,
                            ),

                        "completion_tokens":
                            getattr(
                                usage,
                                "completion_tokens",
                                None,
                            ),

                        "total_tokens":
                            getattr(
                                usage,
                                "total_tokens",
                                None,
                            ),
                    },

                "attempt":
                    attempt,

            }

            return result

        except Exception as e:

            last_error = e

            logger.warning(
                "Attempt %d/%d failed: %s",
                attempt,
                MAX_RETRIES,
                e,
            )

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    logger.exception(
        "LLM generation failed after retries."
    )

    raise RuntimeError(
        f"Generation failed after {MAX_RETRIES} attempts: {last_error}"
    )


def main():
    """
    Smoke test.
    """

    sample = {

        "domain": "finance",

        "instruction":
            "Explain what Bitcoin is to a beginner.",

    }

    response = generate_response(sample)

    print()

    from pprint import pprint
    pprint(response)


if __name__ == "__main__":
    main()