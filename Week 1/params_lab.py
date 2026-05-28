"""
Temperature & Top-p Learning Lab
=================================

Run this file to SEE how temperature and top_p change Bedrock responses.

  python3 params_lab.py

Concepts (simple):
------------------
TEMPERATURE (0.0 to 1.0+)
  - Low  (0.0 - 0.2)  -> predictable, same-ish answers (good for facts)
  - High (0.7 - 1.0)  -> creative, varied wording (good for brainstorming)

TOP_P (nucleus sampling, 0.0 to 1.0)  [Bedrock uses top_p, not top_k]
  - Low  (0.5 - 0.7)  -> model considers fewer word choices -> tighter output
  - High (0.9 - 1.0)  -> more word choices allowed -> more variety

TOP_K (related idea — NOT used in our Nemotron invoke body)
  - Only the top K most likely next words are considered.
  - Many APIs use top_p OR top_k; AWS Bedrock Nemotron uses top_p in invoke_model.

Rule of thumb for THIS week's project:
  - Summarization / Sentiment / Action items -> low temperature + top_p ~ 0.9
  - Creative writing / marketing ideas       -> higher temperature + top_p ~ 0.95
"""

import json
import os
import time
from pathlib import Path

import boto3
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load AWS settings (same as project.py)
# ---------------------------------------------------------------------------
_env_file = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_file)
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "nvidia.nemotron-nano-3-30b")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Fixed sample texts so every run compares fairly (no paste needed)
SAMPLE_SUMMARY_TEXT = """
Team meeting notes: Priya will prepare the Q1 report by Friday.
Ravi will review the budget on Monday. The launch date is March 15.
Marketing still needs final logo approval from the client.
"""

SAMPLE_SENTIMENT_TEXT = """
I am really disappointed with the delayed shipment and poor support.
This was the third time my order arrived late without any update.
"""

SAMPLE_ACTION_TEXT = """
Hi team, please send the slide deck to Anitha before Wednesday.
Ravi, book the conference room for Monday 2pm. No other tasks mentioned.
"""

SAMPLE_CREATIVE_TEXT = """
Write three catchy one-line slogans for a bus route finder app in Coimbatore.
"""


def get_bedrock_client():
    kwargs = {"region_name": AWS_REGION}
    if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
        kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
        kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY
    return boto3.client("bedrock-runtime", **kwargs)


def call_bedrock(prompt: str, temperature: float, top_p: float) -> str:
    client = get_bedrock_client()
    response = client.invoke_model(
        modelId=BEDROCK_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(
            {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 512,
                "temperature": temperature,
                "top_p": top_p,
            }
        ),
    )
    body = json.loads(response["body"].read())
    return body["choices"][0]["message"]["content"]


def print_header(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_run(label: str, temperature: float, top_p: float, response: str):
    print(f"\n--- {label} ---")
    print(f"  temperature = {temperature}  |  top_p = {top_p}")
    print("-" * 50)
    print(response.strip())
    print("-" * 50)


def run_single(prompt: str, temperature: float, top_p: float, label: str):
    """One API call with clear printed output."""
    print(f"\nCalling Bedrock ({label})...")
    try:
        text = call_bedrock(prompt, temperature, top_p)
        print_run(label, temperature, top_p, text)
    except Exception as err:
        print(f"Error: {err}")
    time.sleep(0.5)  # small pause between calls to avoid rate limits


# ---------------------------------------------------------------------------
# SCENARIOS — each teaches one comparison
# ---------------------------------------------------------------------------

def scenario_temperature_sweep():
    """
    Same prompt, different temperatures. top_p fixed at 0.9.
    Watch: low temp = stable facts, high temp = more varied/creative words.
    """
    print_header("SCENARIO 1: Temperature sweep (top_p fixed at 0.9)")
    prompt = f"Summarize in exactly 3 bullet points:\n{SAMPLE_SUMMARY_TEXT}"

    for temp, label in [
        (0.0, "Very low — most deterministic"),
        (0.3, "Recommended for summarization"),
        (0.7, "More creative"),
        (1.0, "Very high — most random"),
    ]:
        run_single(prompt, temp, 0.9, label)


def scenario_top_p_sweep():
    """
    Same prompt, different top_p. temperature fixed at 0.3.
    Watch: low top_p = narrower word choice, high top_p = more diversity.
    """
    print_header("SCENARIO 2: Top-p sweep (temperature fixed at 0.3)")
    prompt = f"Summarize in exactly 3 bullet points:\n{SAMPLE_SUMMARY_TEXT}"

    for top_p, label in [
        (0.5, "Low top_p — tighter vocabulary"),
        (0.9, "Default for this project"),
        (1.0, "Maximum diversity"),
    ]:
        run_single(prompt, 0.3, top_p, label)


def scenario_summarization_good_vs_bad():
    """Factual task: low temp wins. High temp may add ideas not in the text."""
    print_header("SCENARIO 3: Summarization — good vs bad parameters")
    prompt = f"""Summarize in 3 bullet points. Do not add facts not in the text.

Text:
{SAMPLE_SUMMARY_TEXT}"""

    run_single(prompt, 0.2, 0.9, "GOOD: temp=0.2, top_p=0.9")
    run_single(prompt, 0.9, 1.0, "BAD:  temp=0.9, top_p=1.0 (may hallucinate)")


def scenario_sentiment_good_vs_bad():
    """Classification needs consistency — high temp can flip labels."""
    print_header("SCENARIO 4: Sentiment — good vs bad parameters")
    prompt = f"""Return exactly:
Sentiment: Positive, Negative, or Neutral
Reason: one sentence
Confidence: Low, Medium, or High

Text:
{SAMPLE_SENTIMENT_TEXT}"""

    run_single(prompt, 0.0, 0.9, "GOOD: temp=0.0, top_p=0.9")
    run_single(prompt, 0.8, 1.0, "BAD:  temp=0.8, top_p=1.0 (inconsistent)")


def scenario_action_items_good_vs_bad():
    """Extraction must not invent owners/deadlines."""
    print_header("SCENARIO 5: Action items — good vs bad parameters")
    prompt = f"""Extract action items as a markdown table.
Columns: Action Item | Owner | Deadline
Use "Not specified" if missing. Do not invent tasks.

Text:
{SAMPLE_ACTION_TEXT}"""

    run_single(prompt, 0.1, 0.9, "GOOD: temp=0.1, top_p=0.9")
    run_single(prompt, 0.9, 1.0, "BAD:  temp=0.9, top_p=1.0 (may invent rows)")


def scenario_creative_good_vs_bad():
    """Creative task: higher temperature is often helpful."""
    print_header("SCENARIO 6: Creative slogans — good vs bad parameters")
    prompt = SAMPLE_CREATIVE_TEXT.strip()

    run_single(prompt, 0.2, 0.8, "TOO SAFE: temp=0.2 (may repeat similar lines)")
    run_single(prompt, 0.8, 0.95, "GOOD:    temp=0.8 (more varied slogans)")


def scenario_extreme_combinations():
    """Four corners: shows combined effect of both knobs."""
    print_header("SCENARIO 7: Four combinations (same short prompt)")
    prompt = "List 3 benefits of using a bus route app. One short phrase per line."

    combos = [
        (0.0, 0.5, "Robot mode: lowest randomness"),
        (0.0, 1.0, "Focused but diverse words"),
        (1.0, 0.5, "Creative but narrow vocabulary"),
        (1.0, 1.0, "Maximum chaos"),
    ]
    for temp, top_p, label in combos:
        run_single(prompt, temp, top_p, label)


def scenario_same_prompt_twice():
    """
    Run identical settings twice. Low temp should look similar;
    high temp should often differ.
    """
    print_header("SCENARIO 8: Repeat same call — stability test")
    prompt = "Reply with one sentence: What is 2+2?"

    print("\n[Low temp 0.0 — expect nearly identical answers]")
    run_single(prompt, 0.0, 0.9, "Run A")
    run_single(prompt, 0.0, 0.9, "Run B")

    print("\n[High temp 1.0 — answers may differ in wording]")
    run_single(prompt, 1.0, 0.9, "Run A")
    run_single(prompt, 1.0, 0.9, "Run B")


# Map menu number -> scenario function
SCENARIOS = {
    "1": ("Temperature sweep", scenario_temperature_sweep),
    "2": ("Top-p sweep", scenario_top_p_sweep),
    "3": ("Summarization: good vs bad", scenario_summarization_good_vs_bad),
    "4": ("Sentiment: good vs bad", scenario_sentiment_good_vs_bad),
    "5": ("Action items: good vs bad", scenario_action_items_good_vs_bad),
    "6": ("Creative slogans: good vs bad", scenario_creative_good_vs_bad),
    "7": ("Four extreme combinations", scenario_extreme_combinations),
    "8": ("Repeat run stability test", scenario_same_prompt_twice),
}


def show_menu():
    print("\n" + "=" * 70)
    print("  Temperature & Top-p Learning Lab")
    print("=" * 70)
    print(f"  Model: {BEDROCK_MODEL_ID}  |  Region: {AWS_REGION}")
    print("\n  Each scenario calls Bedrock multiple times (uses API quota).\n")
    for key, (name, _) in SCENARIOS.items():
        print(f"  {key}. {name}")
    print("  9. Run ALL scenarios (many API calls)")
    print("  0. Exit")


def read_choice():
    while True:
        raw = input("\nEnter choice (0-9): ").strip()
        if raw in [str(i) for i in range(10)]:
            return raw
        if raw:
            print("(Enter 0-9 only)")


def run_all():
    print_header("RUNNING ALL SCENARIOS")
    for key in sorted(SCENARIOS.keys()):
        name, func = SCENARIOS[key]
        print(f"\n>>> Starting scenario {key}: {name}")
        func()
    print_header("ALL SCENARIOS DONE")
    print_quick_reference()


def print_quick_reference():
    print("""
QUICK REFERENCE
---------------
| Task type              | Temperature | Top-p |
|------------------------|-------------|-------|
| Summarization          | 0.2 - 0.4   | 0.9   |
| Sentiment              | 0.0 - 0.2   | 0.9   |
| Action item extraction | 0.0 - 0.3   | 0.9   |
| Creative / brainstorm  | 0.7 - 1.0   | 0.9+  |

top_k vs top_p: Bedrock Nemotron uses top_p in the API body.
Document experiments in playbook.md after you run these scenarios.
""")


def main():
    print_quick_reference()

    while True:
        show_menu()
        choice = read_choice()

        if choice == "0":
            print("Goodbye!\n")
            break
        if choice == "9":
            confirm = input("This makes ~20+ API calls. Continue? (y/n): ").strip().lower()
            if confirm == "y":
                run_all()
            continue
        if choice in SCENARIOS:
            name, func = SCENARIOS[choice]
            print(f"\nRunning: {name}")
            func()
            print_quick_reference()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
