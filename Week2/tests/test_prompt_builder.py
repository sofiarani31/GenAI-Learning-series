from src.prompt_builder import build_extraction_prompt

def test_build_extraction_prompt():
    user_text = "My wifi is extremely slow and I cannot work."
    prompt = build_extraction_prompt(user_text)
    
    # Verify the user's text was successfully injected into the template
    assert user_text in prompt
    
    # Verify the core instruction boundaries are present
    assert "Return only valid JSON" in prompt
    assert "Schema:" in prompt
    assert "customer_name" in prompt
    assert "action_items" in prompt
