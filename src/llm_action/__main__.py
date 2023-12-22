import json
import os
from pathlib import Path
import string
from typing import Optional
import typer
from openai import AzureOpenAI

from llm_action.models import Comment, Comments
from llm_action.prompt import create_prompt

AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
AZURE_OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
)

# TODO:
# - SYSTEM_INSTRUCTION (how to format output) or fix with pydantic
# - USER_INSTRUCTION Add a way to specify the prompt as a user (review my text, review my python code, make it beautiful, )
#   - Specify via predefined template (python, blogpost, poem)
# - CONTENT: The file to review

# Consider outputting only fileno: comment

PROMPT = string.Template(
    """
Please review my text. For each line, make a suggestion. 
Consider writing style, conciseness and writing style.
If you do, output it as follows:
```shell
::notice file={$filepath},line={lineno},col=1::{comment}
```
Where `lineno` is the line number, and `comment` is what you want to suggest. Replace those values.

Here is the text to review:
"""
)


def comment_as_github_annotation(comment: Comment, file: Path) -> str:
    """
    Create a github notice string from a comment
    By printing the resulting value during the Github action run, the comment will added as an annotation to the file
    See the docs for more details https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-a-notice-message
    """
    s = f"::notice file={file},line={comment.line_start}"
    if comment.line_end:
        s += f",endLine={comment.line_end}"
    s += f"::{comment.content}"
    return s



def get_file_list(pattern: str) -> list[Path]:
    """Get a list of files given a glob pattern"""
    path = Path(".")
    print(path.absolute())
    files = list(path.glob(pattern))
    return files


def query_llm(prompt: str) -> str | None:
    """Query the LLM with the given prompt."""
    # print(prompt)
    completion = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.0,
    )
    return completion.choices[0].message.content


def read_file(path: Path) -> Optional[str]:
    with path.open() as f:
        content = f.read()
        if len(content) == 0:
            print("File is empty!")
            return
    return content


def review_content(content: str, user_instruction: Optional[str]) -> list[Comment]:
    """Review the given content and return a list of comments"""

    prompt = create_prompt(content, user_instruction=user_instruction)
    llm_output = query_llm(prompt)
    if not llm_output:
        return []
    comments = Comments.model_validate_json(llm_output).root
    return comments


def main(glob_pattern: str, user_instruction: Optional[str] = None) -> None:
    files = get_file_list(glob_pattern)
    if not files:
        print(f"No files found for pattern '{glob_pattern}'")
        raise typer.Exit()

    print(f"Found {len(files)} files for pattern '{glob_pattern}'")

    for file in files:
        print(f"Reviewing file {file}")
        content = read_file(file)
        if not content:
            # Empty file or file not found
            continue
        comments = review_content(content, user_instruction=user_instruction)
        for comment in comments:
            print(comment_as_github_annotation(comment, file))


if __name__ == "__main__":
    typer.run(main)
