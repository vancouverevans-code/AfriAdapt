"""
AfriBench Prompt Builder

Generates high-quality benchmark prompts for evaluating
LLMs on African languages and domains.
"""

import json


EXAMPLE_OUTPUT = {
    "instruction": (
        "A farmer in Kisumu notices yellow streaks on maize leaves after "
        "two weeks of heavy rainfall. Explain the likely causes and "
        "recommend practical actions."
    ),
    "reference_answer": (
        "Yellow streaks may indicate maize streak virus, nutrient deficiency, "
        "or prolonged waterlogging. Recommend inspecting plants, improving "
        "drainage, performing a soil test, applying nutrients where "
        "appropriate, removing infected plants when necessary, using "
        "certified seed for future planting, and consulting a local "
        "agricultural extension officer."
    ),
    "evaluation_criteria": {
        "accuracy": (
            "Correctly identifies likely causes and appropriate treatments."
        ),
        "local_context": (
            "Recommendations are suitable for East African farming conditions."
        ),
        "clarity": (
            "Response is easy to understand and logically structured."
        ),
        "completeness": (
            "Covers diagnosis, explanation, and actionable recommendations."
        ),
        "safe_response": (
            "Avoids harmful or misleading agricultural advice."
        ),
    },
}


SCHEMA = {
    "instruction": "string",
    "reference_answer": "string",
    "evaluation_criteria": {
        "accuracy": "string",
        "local_context": "string",
        "clarity": "string",
        "completeness": "string",
        "safe_response": "string",
    },
}


def build_prompt(
    domain: str,
    language: str,
    difficulty: str,
    skill: str,
):
    """
    Build a benchmark generation prompt for the LLM.
    """

    return f"""
You are an expert AI benchmark engineer.

Your job is to create ONE high-quality benchmark example
for evaluating large language models.

==========================================================
BENCHMARK SETTINGS
==========================================================

Domain:
{domain}

Language:
{language}

Difficulty:
{difficulty}

Skill:
{skill}

==========================================================
OBJECTIVE
==========================================================

Create ONE realistic benchmark example.

The benchmark should evaluate whether an AI model can
reason correctly while understanding African contexts.

==========================================================
BENCHMARK REQUIREMENTS
==========================================================

The instruction MUST:

• Be realistic.

• Require reasoning instead of memorization.

• Be culturally authentic.

• Use African names, locations, currencies,
  institutions or situations whenever appropriate.

• Avoid stereotypes.

• Be challenging enough for the selected difficulty.

• Match the requested skill.

==========================================================
REFERENCE ANSWER
==========================================================

The reference answer should:

• Be factually correct.

• Be complete.

• Be concise.

• Be educational.

• Be safe.

• Be the ideal ("gold standard") answer.

==========================================================
EVALUATION CRITERIA
==========================================================

Provide short descriptions for each field.

accuracy

local_context

clarity

completeness

safe_response

==========================================================
OUTPUT FORMAT
==========================================================

Return ONLY valid JSON.

DO NOT write explanations.

DO NOT write markdown.

DO NOT use code fences.

DO NOT add comments.

The JSON MUST exactly follow this schema:

{json.dumps(SCHEMA, indent=2)}

==========================================================
EXAMPLE
==========================================================

This is ONLY an example of the required structure.

Do NOT copy it.

{json.dumps(EXAMPLE_OUTPUT, indent=2, ensure_ascii=False)}

==========================================================
IMPORTANT
==========================================================

Generate a completely NEW benchmark.

Do NOT repeat the example.

Return ONLY the JSON object.

Nothing else.
"""