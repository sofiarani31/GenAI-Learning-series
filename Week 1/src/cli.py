from rich.console import Console
from src.prompt_loader import load_prompt
import boto3
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from src.llm_client import invoke_model
# from llm_client import bedrock_client

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

load_dotenv()

console = Console()

def show_menu():
    console.print("\n[bold cyan]Choose a task:[/bold cyan]")
    console.print("1. Summarization")
    console.print("2. Sentiment Analysis")
    console.print("3. Action Item Extraction")
    console.print("4. Exit")

TASK_PROMPTS = {
    "1": "summarization_prompt.txt",
    "2": "sentiment_prompt.txt",
    "3": "action_items_prompt.txt"
}

def run_cli():

    while True:

        show_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "4":
            print("Goodbye!")
            break

        if choice not in TASK_PROMPTS:
            print("Ignored - Enter only 1, 2, 3, or 4.")
            continue

        user_text = input("\nPaste your text:\n")

        if not user_text.strip():
            print("Input cannot be empty")
            continue

        temperature = input("Temperature [default 0.3]: ").strip()
        top_p = input("Top-p [default 0.9]: ").strip()

        temperature = float(temperature) if temperature else 0.3
        top_p = float(top_p) if top_p else 0.9

        prompt = load_prompt(
            TASK_PROMPTS[choice],
            user_text
        )

        print("\nProcessing...\n")

        result = invoke_model(
            prompt,
            temperature,
            top_p
        )

        print(result)

if __name__ == "__main__":
    run_cli()