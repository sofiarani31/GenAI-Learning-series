import os

def build_extraction_prompt(user_text: str) -> str:
    """
    Reads the extraction prompt template and injects the user_text into it.
    """
    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        "prompts", 
        "extraction_prompt.txt"
    )
    
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()
        
    # Replace the {user_text} placeholder with the actual text
    # We use replace instead of .format() to avoid issues with curly braces in the JSON schema
    return prompt_template.replace("{user_text}", user_text)
