"""
Prompt builder for AfriBench.
"""

from textwrap import dedent


def build_prompt(domain, language, difficulty, skill):
    return dedent(f"""
    You are helping build AfriBench v1,
    an evaluation benchmark for African AI systems.

    Generate ONE benchmark example.

    Domain:
    {domain}

    Language:
    {language}

    Difficulty:
    {difficulty}

    Skill:
    {skill}

    Requirements

    - African context
    - Realistic scenario
    - Requires reasoning
    - Avoid trivia
    - Avoid subjective opinions
    - Safe
    - Useful for evaluating instruction tuned models

    Return ONLY valid JSON.

    {{
      "instruction":"",
      "reference_answer":"",
      "evaluation_criteria": {{
          "accuracy": true,
          "local_context": true,
          "clarity": true,
          "completeness": true,
          "safe_response": true
      }}
    }}
    """).strip()