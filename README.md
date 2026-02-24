# OpenAI Python Code Reviewer

A command-line tool that uses the OpenAI Python SDK to perform structured code reviews on any Python file. Built as a companion project for the [RealPython](https://realpython.com/) Sample tutorial *"How to Use the OpenAI Python SDK to Review Your Own Python Code"*.

## What It Does

Point the script at any `.py` file and GPT-4o reviews it for, correctness, error handling, security, Pythonic style, and maintainability, and prints severity-ranked feedback directly in your terminal.

```bash
python review.py data_parser.py
```
# Structure
```
code-reviewer/
├── .venv/           # Virtual environment (required)
├── .env             # Your API key (optional)
├── data_parser.py   # Sample Python file used in the tutorial
├── users.csv        # Sample data file for data_parser.py
└── review.py        # The code reviewer script
```

# Requirements

* Python 3.10+

* An [OpenAI account](https://platform.openai.com/account/billing) with a funded [API key](https://platform.openai.com/api-keys)

# Setup

Clone or download this project and navigate into the folder:

`cd code-reviewer`

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```
## Install dependencies:

`pip install openai python-dotenv`

## Add your API key to a .env file:

`OPENAI_API_KEY="your-api-key-here"`

Get your key at: https://platform.openai.com/api-keys

## Usage

Run the reviewer against any Python file:

```bash 
python review.py <path_to_file.py>
```

Example:

```bash
python review.py data_parser.py
```

**Sample Output**

![Sample Output](sample_reviewer_output.png)

```
python3 reviewer.py data_parser.py 
Reviewing 'data_parser.py' with gpt-4o...

============================================================
  CODE REVIEW: data_parser.py
  Model: gpt-4o
============================================================

**[CRITICAL] Line 8 — ERROR HANDLING**  
Problem: File is opened without a context manager, which can lead to resource leaks if an exception occurs.  
Why it matters: Failing to close files can exhaust system resources and lead to unpredictable behavior.  
Recommendation: Use a `with` statement to open the file, which ensures it is properly closed.

**[CRITICAL] Line 58 — ERROR HANDLING**  
Problem: Division by zero is possible if `len(records)` is zero in `get_average_age`.  
Why it matters: This will raise a `ZeroDivisionError`, causing the program to crash.  
Recommendation: Add a check to ensure `len(records)` is not zero before performing the division.

**[WARNING] Line 43 — ERROR HANDLING**  
Problem: File is opened without a context manager in `save_to_json`.  
Why it matters: Similar to the previous issue, this can lead to resource leaks.  
Recommendation: Use a `with` statement to open the file, ensuring it is properly closed.

**[WARNING] Line 11 — MAINTAINABILITY**  
Problem: The function `read_csv` lacks error handling for file operations.  
Why it matters: If the file does not exist or is unreadable, the function will raise an unhandled exception.  
Recommendation: Add a try/except block to handle `IOError` or `FileNotFoundError`.

**[WARNING] Line 28 — ERROR HANDLING**  
Problem: The function `normalize_age` assumes all records have a valid "age" field that can be converted to an integer.  
Why it matters: If "age" is missing or not a valid integer, this will raise a `ValueError`.  
Recommendation: Add error handling to manage cases where "age" is missing or invalid.

**[SUGGESTION] Line 3 — SECURITY**  
Problem: The script uses hardcoded file paths, which can be a security risk if paths are not validated.  
Why it matters: Hardcoded paths can lead to directory traversal vulnerabilities if user input is incorporated.  
Recommendation: Validate and sanitize file paths before use, especially if they are derived from user input.

**[SUGGESTION] Line 1 — PYTHONIC STYLE**  
Problem: The module name `data_parser.py` does not match the filename `dataparser.py`.  
Why it matters: Consistency in naming improves readability and maintainability.  
Recommendation: Rename the file to match the module name or vice versa.

**[SUGGESTION] Line 65 — MAINTAINABILITY**  
Problem: The `load_and_process` function does multiple things: reading, normalizing, and filtering data.  
Why it matters: Functions that do too many things are harder to test and maintain.  
Recommendation: Consider breaking this function into smaller, more focused functions.

**SUMMARY**  
The code has several critical issues related to file handling and potential division by zero errors, which could lead to resource leaks and crashes. Error handling is generally lacking, especially in functions that assume valid input without checks. The code could benefit from improved maintainability by breaking down complex functions and ensuring consistency in naming conventions.```
