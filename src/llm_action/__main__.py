import os
from pathlib import Path
import string
import typer
from openai import AzureOpenAI

AZURE_OPENAI_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
AZURE_OPENAI_API_VERSION = os.environ["AZURE_OPENAI_API_VERSION"]

client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
)

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


def get_file_list(pattern: str) -> list[Path]:
    path = Path(".")
    print(path.absolute())
    files = list(path.glob(pattern))
    return files


def query_llm(prompt: str) -> str | None:
    """Query the LLM with the given prompt."""
    print(prompt)
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


def review_file(path: Path) -> None:
    with path.open() as f:
        content = f.read()
        if len(content) == 0:
            print("File is empty!")
            return
    llm_input = PROMPT.substitute(filepath=path) + content
    llm_output = query_llm(llm_input)
    print(llm_output)  # Printing the output will comment it on the PR


def main(glob_pattern: str) -> None:
    files = get_file_list(glob_pattern)
    if not files:
        print(f"No files found for pattern '{glob_pattern}'")
        raise typer.Exit()

    print(f"Found {len(files)} files for pattern '{glob_pattern}'")

    for file in files:
        print(f"Reviewing file {file}")
        review_file(file)


if __name__ == "__main__":
    typer.run(main)
