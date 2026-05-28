# pip install boto3
# pip install python-dotenv
# pip install rich

import json
import os
from pathlib import Path

import boto3
from dotenv import load_dotenv
from rich.console import Console

console = Console()
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "nvidia.nemotron-nano-3-30b")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

_client_kwargs = {"region_name": AWS_REGION}
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    _client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
    _client_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

bedrock_client = boto3.client("bedrock-runtime", **_client_kwargs)

TASK_PROMPTS = {
    "1": "summarization_prompt.txt",
    "2": "sentiment_prompt.txt",
    "3": "action_items_prompt.txt",
}

TASK_DEFAULTS = {
    "1": {"temperature": 0.3, "top_p": 0.9},
    "2": {"temperature": 0.1, "top_p": 0.9},
    "3": {"temperature": 0.2, "top_p": 0.9},
}


def load_prompt(filename: str, user_text: str) -> str:
    template = (PROMPTS_DIR / filename).read_text(encoding="utf-8")
    return template.format(user_text=user_text.strip())


def invoke_model(prompt: str, temperature: float, top_p: float) -> str:
    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
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


def show_menu():
    console.print("\n[bold cyan]Choose a task:[/bold cyan]")
    console.print("1. Summarization")
    console.print("2. Sentiment Analysis")
    console.print("3. Action Item Extraction")
    console.print("4. Exit")


def run_cli():
    console.print("\n[bold]Welcome to the Prompt Engineering CLI[/bold]")
    console.print(f"Model: {MODEL_ID} | Region: {AWS_REGION}")

    while True:
        show_menu()
        choice = input("\nEnter your choice: ").strip()

        if choice == "4":
            console.print("Goodbye!")
            break

        if choice not in TASK_PROMPTS:
            console.print("[red]Invalid choice[/red]")
            continue

        user_text = input("\nPaste your text:\n")
        if not user_text.strip():
            console.print("[red]Input cannot be empty[/red]")
            continue

        defaults = TASK_DEFAULTS[choice]
        temperature = input(f"Temperature [default {defaults['temperature']}]: ").strip()
        top_p = input(f"Top-p [default {defaults['top_p']}]: ").strip()

        temperature = float(temperature) if temperature else defaults["temperature"]
        top_p = float(top_p) if top_p else defaults["top_p"]

        prompt = load_prompt(TASK_PROMPTS[choice], user_text)

        console.print("\n[yellow]Processing...[/yellow]\n")
        try:
            result = invoke_model(prompt, temperature, top_p)
        except Exception as err:
            console.print(f"[red]Error calling Bedrock: {err}[/red]")
            continue

        console.print("[bold green]Result:[/bold green]")
        console.print("-" * 40)
        console.print(result)
        console.print("-" * 40)


if __name__ == "__main__":
    run_cli()
