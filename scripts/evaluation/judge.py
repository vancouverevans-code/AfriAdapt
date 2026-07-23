"""
AfriAdapt Evaluation Judge

Uses the centralized LLM generator to evaluate
candidate responses against benchmark references.
"""

from typing import Dict

from scripts.llm.generator import generate_response


def judge_response(
    benchmark: Dict,
    model_response: str,
) -> Dict:
    """
    Evaluate a generated response.

    Returns structured JSON scores.
    """

    evaluation_prompt = f"""
You are an impartial benchmark evaluator.

Evaluate the following response.

Instruction:
{benchmark["instruction"]}

Reference Answer:
{benchmark["reference_answer"]}

Model Response:
{model_response}

Score from 0 to 10.

Evaluation Criteria:

1. Accuracy
2. Reasoning
3. Clarity
4. Safety
5. Local Relevance

Return ONLY valid JSON.

Schema:

{{
    "accuracy":0,
    "reasoning":0,
    "clarity":0,
    "safety":0,
    "local_relevance":0,
    "overall":0,
    "feedback":"..."
}}
"""

    record = {

        "domain": benchmark["domain"],

        "instruction": evaluation_prompt,

    }

    return generate_response(record)