from pathlib import Path

PROMPT_DIR = Path("prompts")

def load_prompt(filename, user_text):
    prompt_path = PROMPT_DIR / filename

    with open(prompt_path, "r", encoding="utf-8") as file:
        template = file.read()

    return template.format(user_text=user_text)