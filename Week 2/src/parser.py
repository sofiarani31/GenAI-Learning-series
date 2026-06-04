import json
from pydantic import ValidationError
from src.schemas import ExtractedRecord

def parse_and_validate(raw_response: str) -> ExtractedRecord:
    """
    Cleans the raw response, parses it as JSON, and validates it against the Pydantic schema.
    """
    # 1. Clean potential markdown wrapping (e.g. ```json ... ```)
    # AI models sometimes ignore prompts and wrap JSON in markdown anyway.
    clean_text = raw_response.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    elif clean_text.startswith("```"):
        clean_text = clean_text[3:]
        
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    
    clean_text = clean_text.strip()
    
    try:
        # 2. Parse standard JSON string to a Python dictionary
        parsed_dict = json.loads(clean_text)
        
        # 3. Validate the dictionary matches our enterprise schema
        validated_record = ExtractedRecord.model_validate(parsed_dict)
        return validated_record
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from model response: {e}\nRaw Response: {raw_response}")
    except ValidationError as e:
        raise ValueError(f"JSON did not match the expected schema: {e}")
