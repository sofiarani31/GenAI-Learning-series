"""
Week 1: Prompt Engineering CLI

A simple command-line app that:
  1. Accepts raw text from the user
  2. Fills a prompt template for the chosen task
  3. Sends the prompt to AWS Bedrock
  4. Prints the model response

Tasks: Summarization, Sentiment Analysis, Action Item Extraction
"""

import json
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

# Load .env from project root (parent folder) or current directory
_env_file = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_file)
load_dotenv()

# ---------------------------------------------------------------------------
# AWS Bedrock settings (from .env)
# ---------------------------------------------------------------------------
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "nvidia.nemotron-nano-3-30b")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Default inference settings per task (see playbook.md for why)
TASK_DEFAULTS = {
    "1": {"name": "Summarization", "temperature": 0.3, "top_p": 0.9},
    "2": {"name": "Sentiment Analysis", "temperature": 0.1, "top_p": 0.9},
    "3": {"name": "Action Item Extraction", "temperature": 0.2, "top_p": 0.9},
}

# ---------------------------------------------------------------------------
# Parameterized prompt templates — use {user_text} for the user's input
# ---------------------------------------------------------------------------
PROMPT_TEMPLATES = {
    "1": """You are a helpful assistant that summarizes text clearly.

Task:
Summarize the text in 3-5 bullet points.

Rules:
- Keep the summary concise.
- Preserve the main ideas.
- Do not add information that is not in the text.
- Use simple language.

Text:
{user_text}""",
    "2": """You are a sentiment analysis assistant.

Task:
Analyze the sentiment of the text.

Return the output in this exact format:
Sentiment: Positive, Negative, or Neutral
Reason: One short sentence
Confidence: Low, Medium, or High

Text:
{user_text}""",
    "3": """You are an assistant that extracts action items from text.

Task:
Extract all action items from the text.

Return the output as a markdown table with these columns:
Action Item | Owner | Deadline

Rules:
- Only extract tasks that are clearly mentioned.
- If owner is missing, write "Not specified".
- If deadline is missing, write "Not specified".
- Do not create action items that are not present in the text.

Text:
{user_text}""",
}


def get_bedrock_client():
    """Create a Bedrock Runtime client using .env credentials if provided."""
    kwargs = {"region_name": AWS_REGION}
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    return boto3.client("bedrock-runtime", **kwargs)


def call_bedrock(prompt: str, temperature: float, top_p: float) -> str:
    """
    Send a prompt to Bedrock and return the assistant's reply text.
    Uses invoke_model with a messages-style body (Nemotron format).
    """
    client = get_bedrock_client()
    response = client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(
            {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2048,
                "temperature": temperature,
                "top_p": top_p,
            }
        ),
    )
    body = json.loads(response["body"].read())
    return body["choices"][0]["message"]["content"]


def build_prompt(task_choice: str, user_text: str) -> str:
    """Insert user text into the template for the selected task."""
    template = PROMPT_TEMPLATES[task_choice]
    return template.format(user_text=user_text.strip())


# Type this on its own line when done pasting (blank lines in text are OK)
END_MARKER = "END"


def read_multiline_text() -> str:
    """
    Read pasted or typed text until the user types END on its own line.
    Using a blank line would stop too early when the text has empty paragraphs.
    """
    print("Paste or type your text below.")
    print(f"When finished, type {END_MARKER} on a new line and press Enter:\n")
    lines = []
    while True:
        line = input()
        if line.strip() == END_MARKER:
            break
        lines.append(line)
    return "\n".join(lines)


def read_menu_choice() -> str:
    """
    Read menu choice (1-4). Ignores stray lines left in stdin from a bad paste,
    so the menu does not spin on 'Invalid choice' for every leftover line.
    """
    while True:
        raw = int(input("\nEnter your choice (1-4): ").strip())
        if raw in ("1", "2", "3", "4"):
            return raw
        if raw:
            print("(Ignored — enter only 1, 2, 3, or 4)")


def ask_float(prompt: str, default: float) -> float:
    """Ask for a number; use default if user presses Enter."""
    raw = input(f"\n{prompt} [default: {default}]: ").strip()
    if raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        print("Invalid number, using default.")
        return default


def run_task(task_choice: str):
    """Run one CLI task: get input, build prompt, call Bedrock, print result."""
    task = TASK_DEFAULTS[task_choice]
    print(f"\n--- {task['name']} ---\n")

    user_text = read_multiline_text()
    if not user_text.strip():
        print("No text provided. Going back to menu.\n")
        return

    # Ask parameters on separate lines (after all text is entered)
    temperature = ask_float("Temperature", task["temperature"])
    top_p = ask_float("Top-p", task["top_p"])

    final_prompt = build_prompt(task_choice, user_text)

    print("\nProcessing...\n")
    try:
        result = call_bedrock(final_prompt, temperature, top_p)
    except Exception as err:
        print(f"Error calling Bedrock: {err}\n")
        return

    print("Result:")
    print("-" * 40)
    print(result)
    print("-" * 40)
    print()


def show_menu():
    """Print the main menu."""
    print("\nWelcome to the Prompt Engineering CLI\n")
    print("Choose a task:")
    print("  1. Summarization")
    print("  2. Sentiment Analysis")
    print("  3. Action Item Extraction")
    print("  4. Exit")


def main():
    """Main loop: show menu, run task, repeat until exit."""
   

    print("Using model:", BEDROCK_MODEL_ID, "| Region:", AWS_REGION)

    while True:
        show_menu()
        choice = read_menu_choice()

        if choice == "4":
            print("Goodbye!\n")
            break
        run_task(choice)


if __name__ == "__main__":
    main()
