import json
from typing import Optional

from llm_review.models import Comments

SYSTEM_INSTRUCTION = f"""
Review a file, by commenting on single or multiple lines.
Prefer to comment on multiple lines.
Don't comment on every line.
Don't not repeat yourself.
Provide suggestions and examples.
Consider the whole file and use it as context.
Your answer must be valid JSON.

You MUST provide your output according to the following json schema:
```json
[
    {json.dumps(Comments.model_json_schema(), indent=4)}
]
```
Do not include backticks in your answer.
Only provide valid JSON.
"""

POST_PROMPT = """
Here is your input:
"""


def create_prompt(content: str, user_instruction: Optional[str] = None) -> str:
    """Dynamically create a prompt, given a system prompt, a user instruction and content to review."""
    if user_instruction:
        user_instruction = "Here are some additional instructions:\n" + user_instruction
    else:
        user_instruction = ""
    return "\n".join([SYSTEM_INSTRUCTION, user_instruction, POST_PROMPT, content])
