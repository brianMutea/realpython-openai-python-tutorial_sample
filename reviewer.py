
# optional from .env file is used:
#     from dotenv import load_dotenv
#     load_dotenv()

import os
import sys
from pathlib import Path

from openai import OpenAI, OpenAIError


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "gpt-4o"
MAX_TOKENS = 2048

# Approximate character limit before we warn the user about token cost.
# At roughly 4 characters per token, 12000 chars ~ 3000 tokens input.
MAX_FILE_CHARS = 12_000

SYSTEM_PROMPT = """
You are a senior Python developer conducting a thorough code review.
Your job is to identify real problems — not nitpicks — that would be
flagged in a professional pull request.

Review the code across these five dimensions:

1. CORRECTNESS — Logic errors, incorrect assumptions, wrong return values
2. ERROR HANDLING — Missing try/except, unhandled edge cases, silent failures,
   division by zero, missing file checks, type errors at runtime
3. SECURITY — Hardcoded secrets, unsafe file operations, injection risks,
   unvalidated input
4. PYTHONIC STYLE — PEP 8 violations, use of anti-patterns, missed use of
   context managers (with statements), list/dict comprehensions where
   appropriate, type hints missing on public functions
5. MAINTAINABILITY — Unclear variable names, missing or misleading docstrings,
   functions doing too many things, magic numbers or strings

Format your response exactly like this for each issue found:

[SEVERITY] Line X — Category
Problem: <one sentence describing what is wrong>
Why it matters: <one sentence explaining the consequence>
Recommendation: <one sentence explaining what to do instead>

Severity levels: CRITICAL | WARNING | SUGGESTION

After all issues, add a brief SUMMARY section (3 sentences max) with an
overall assessment.

Be direct. Do not rewrite the code. Do not praise what works correctly.
""".strip()


def read_source_file(filepath: str) -> str:
    """
    Read a Python source file from disk and return its contents.

    Args:
        filepath: Path to the .py file to read.

    Returns:
        The file contents as a string.

    Raises:
        SystemExit: If the file does not exist, is not a .py file,
                    or cannot be read.
    """
    path = Path(filepath)

    if not path.exists():
        print(f"Error: File not found — '{filepath}'")
        sys.exit(1)

    if path.suffix != ".py":
        print(f"Error: Expected a .py file, got '{path.suffix}'")
        sys.exit(1)

    try:
        contents = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"Error: Could not read file — {e}")
        sys.exit(1)

    if not contents.strip():
        print("Error: The file is empty.")
        sys.exit(1)

    return contents


def warn_if_large(source_code: str) -> None:
    """
    Print a cost warning if the file exceeds the recommended size limit.

    Args:
        source_code: The Python source code to check.
    """
    char_count = len(source_code)
    if char_count > MAX_FILE_CHARS:
        print(
            f"Warning: This file is {char_count:,} characters. "
            f"Large files consume more API tokens and may increase cost.\n"
        )


def build_user_prompt(source_code: str, filename: str) -> str:
    """
    Build the user-facing prompt that includes the source code.

    Args:
        source_code: The Python source code to review.
        filename: The name of the file being reviewed (for context).

    Returns:
        A formatted prompt string ready to send to the API.
    """
    return (
        f"Please review the following Python file: `{filename}`\n\n"
        f"```python\n{source_code}\n```"
    )


def run_code_review(source_code: str, filename: str) -> str:
    """
    Send the source code to GPT-4o and return the structured review.

    Args:
        source_code: The Python source code to review.
        filename: The filename to include in the prompt for context.

    Returns:
        The model's review as a plain string.

    Raises:
        SystemExit: If the API call fails for any reason.
    """
    client = OpenAI()

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=0.2,  # Lower temperature = more consistent, focused output
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(source_code, filename)},
            ],
        )
    except OpenAIError as e:
        print(f"OpenAI API error: {e}")
        sys.exit(1)

    return response.choices[0].message.content


def print_review(review: str, filename: str) -> None:
    """
    Print the review to stdout with a clear header and footer.

    Args:
        review: The review text returned by the model.
        filename: The filename that was reviewed.
    """
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"  CODE REVIEW: {filename}")
    print(f"  Model: {MODEL}")
    print(f"{separator}\n")
    print(review)
    print(f"\n{separator}\n")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python review.py <path_to_file.py>")
        sys.exit(1)

    filepath = sys.argv[1]
    filename = Path(filepath).name

    source_code = read_source_file(filepath)
    warn_if_large(source_code)

    print(f"Reviewing '{filename}' with {MODEL}...")

    review = run_code_review(source_code, filename)
    print_review(review, filename)


if __name__ == "__main__":
    main()