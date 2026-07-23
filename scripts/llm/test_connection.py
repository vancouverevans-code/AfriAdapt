import json

from scripts.llm.client import client
from scripts.llm.config import MODEL
from scripts.llm.prompts import SYSTEM_PROMPT

response = client.chat.completions.create(
    model=MODEL,
    temperature=0.3,
    max_tokens=150,
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "Explain Bitcoin in two sentences.",
        },
    ],
)

content = response.choices[0].message.content

print("Raw Response:\n")
print(content)

print("\nParsed JSON:\n")
print(json.loads(content))