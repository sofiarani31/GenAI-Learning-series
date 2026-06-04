import pytest
from src.parser import parse_and_validate
from src.schemas import ExtractedRecord

def test_parse_valid_json():
    raw_response = """
    {
      "customer_name": "Jane Doe",
      "issue_type": "Billing",
      "priority": "High",
      "summary": "Charged twice",
      "sentiment": "Negative",
      "action_items": []
    }
    """
    record = parse_and_validate(raw_response)
    assert isinstance(record, ExtractedRecord)
    assert record.customer_name == "Jane Doe"
    assert record.issue_type == "Billing"

def test_parse_markdown_wrapped_json():
    raw_response = """```json
    {
      "customer_name": "Jane Doe",
      "issue_type": "Billing",
      "priority": "High",
      "summary": "Charged twice",
      "sentiment": "Negative",
      "action_items": []
    }
    ```"""
    record = parse_and_validate(raw_response)
    assert record.customer_name == "Jane Doe"

def test_parse_invalid_json():
    raw_response = "{ this is not json"
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        parse_and_validate(raw_response)

def test_parse_invalid_schema():
    # Missing action_items field entirely, which should trigger a Pydantic ValidationError
    raw_response = """
    {
      "customer_name": "Jane Doe",
      "issue_type": "Billing",
      "priority": "High",
      "summary": "Charged twice",
      "sentiment": "Negative"
    }
    """
    with pytest.raises(ValueError, match="JSON did not match the expected schema"):
        parse_and_validate(raw_response)
