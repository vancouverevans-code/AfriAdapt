"""
LLM Response Generator

Production-ready OpenRouter client used across AfriAdapt.
"""

import json
import time
from typing import Dict, Optional

from scripts.llm.client import client
from scripts.llm.config import (
    MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

from scripts.llm.prompts import get_system_prompt
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

    if "instruction" not in record:
        raise ValueError("Record missing 'instruction'.")

    metadata = record.get("metadata", {})

    domain = metadata.get(
        "domain",
        record.get("domain", "general"),
    )

    model_name = model or MODEL
    temp = TEMPERATURE if temperature is None else temperature
    tokens = MAX_TOKENS if max_tokens is None else max_tokens

    logger.info("Generating response | domain=%s", domain)

    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):

        start = time.perf_counter()

        try:

            response = client.chat.completions.create(

                model=model_name,

                temperature=temp,

                max_tokens=tokens,

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

            # -----------------------------
            # Validate response
            # -----------------------------

            if response is None:
                raise RuntimeError(
                    "OpenRouter returned None."
                )

            if not hasattr(response, "choices"):
                raise RuntimeError(
                    "Missing choices field."
                )

            if response.choices is None:
                raise RuntimeError(
                    "choices is None."
                )

            if len(response.choices) == 0:
                raise RuntimeError(
                    "choices list is empty."
                )

            message = response.choices[0].message

            if message is None:
                raise RuntimeError(
                    "message is None."
                )

            content = message.content

            if not content:
                raise RuntimeError(
                    "Empty model response."
                )

            try:
                result = json.loads(content)

            except json.JSONDecodeError:

                result = {
                    "answer": content
                }

            usage = getattr(
                response,
                "usage",
                None,
            )

            result["_metadata"] = {

                "model": model_name,

                "temperature": temp,

                "latency_seconds": elapsed,

                "attempt": attempt,

                "token_usage": None if usage is None else {

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

                time.sleep(
                    RETRY_DELAY * attempt
                )

    logger.exception(
        "LLM generation failed after retries."
    )

    raise RuntimeError(
        f"Generation failed after {MAX_RETRIES} attempts: {last_error}"
    )


def main():

    sample = {

        "domain": "finance",

        "instruction":
            "Explain Bitcoin in simple terms.",

    }

    response = generate_response(sample)

    print(
        json.dumps(
            response,
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()