import json
from typing import Optional

from llm_action.models import Comments

SYSTEM_INSTRUCTION = f"""
You will review a file in a pull request using single or multiline comments.

Consider the whole text, and write a comment or suggestion for the lines you want to review.

You MUST provide your output according to the following json schema:
```json
[
    {json.dumps(Comments.model_json_schema(), indent=4)}
]
```
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
