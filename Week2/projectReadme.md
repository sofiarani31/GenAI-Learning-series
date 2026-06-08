# Week 2 Project: Automated Data Extractor & JSON Parser

## Project Focus

This project focuses on integrating commercial or open APIs such as AWS Bedrock using official SDKs. The application should process unformatted textual logs or customer service conversations asynchronously, handle rate limits safely, and return reliable structured JSON responses.

The final output should be validated as Pydantic objects that follow a predefined enterprise JSON schema.

## Project Goal

Build an application that accepts messy text input, sends it to an AI model, extracts important information, and converts the result into clean structured JSON.

Example inputs:

- Customer support conversations
- Error logs
- Chat transcripts
- Incident reports
- Call center notes

Example output:

```json
{
  "customer_name": "John Smith",
  "issue_type": "Billing",
  "priority": "High",
  "summary": "Customer was charged twice for the monthly subscription.",
  "action_items": [
    {
      "task": "Review duplicate transaction",
      "owner": "Billing team",
      "deadline": "Not specified"
    }
  ],
  "sentiment": "Negative"
}
```

## What The Project Should Look Like

The project should behave like a small enterprise data extraction tool.

User flow:

1. User provides raw unformatted text.
2. App sends the text to Bedrock asynchronously.
3. Model returns structured JSON.
4. App validates the JSON with Pydantic.
5. App prints or saves the validated structured result.

Terminal example:

```bash
python main.py
```

```text
Paste customer conversation or log:
Customer says they were charged twice and need help urgently...

Processing...

Validated JSON Output:
{
  "issue_type": "Billing",
  "priority": "High",
  "sentiment": "Negative"
}
```


## Main Components

### 1. `main.py`

This file starts the app. It should collect input, call the async extraction pipeline, and display the final validated JSON.

Responsibilities:

- Read user input
- Call the extractor
- Print validated JSON
- Handle high-level errors

### 2. `src/config.py`

Stores environment configuration.

Example values:

```text
AWS_REGION=ap-southeast-2
BEDROCK_MODEL_ID=nvidia.nemotron-nano-3-30b
MAX_CONCURRENT_REQUESTS=3
MAX_RETRIES=3
```

Do not hardcode secrets inside Python files.

### 3. `src/bedrock_client.py`

Handles all communication with AWS Bedrock.

Responsibilities:

- Create Bedrock Runtime client using `boto3`
- Send prompts to the model
- Support async processing using `asyncio`
- Retry failed requests when needed
- Return raw model responses

### 4. `src/schemas.py`

Defines the enterprise JSON schema using Pydantic.

Example:

```python
from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: str
    deadline: str


class ExtractedRecord(BaseModel):
    customer_name: str | None
    issue_type: str
    priority: str
    summary: str
    sentiment: str
    action_items: list[ActionItem]
```

This ensures the AI output is not just JSON-looking text, but valid structured data.

### 5. `src/prompt_builder.py`

Builds the prompt sent to the model.

The prompt should clearly tell the model:

- Return only valid JSON
- Do not include markdown
- Follow the exact schema
- Use `"Not specified"` when information is missing
- Do not invent missing data

### 6. `src/parser.py`

Converts the model output into a Pydantic object.

Responsibilities:

- Parse JSON string
- Validate with Pydantic
- Handle invalid JSON
- Ask model to repair JSON if needed

### 7. `src/rate_limiter.py`

Protects the app from sending too many requests at once.

Recommended approach:

- Use `asyncio.Semaphore`
- Limit concurrent requests
- Add retry with exponential backoff
- Handle throttling errors from Bedrock

## Asynchronous Request Design

The app should support processing multiple text records at once.

Example:

```text
Input file contains 20 conversations
App processes 3 at a time
Each result is validated and collected
Final output is a JSON list
```

Recommended flow:

```text
Raw Texts
   ↓
Create Async Tasks
   ↓
Rate Limiter / Semaphore
   ↓
Bedrock API Call
   ↓
JSON Parse
   ↓
Pydantic Validation
   ↓
Final Structured Output
```

## Handling Rate Limits

APIs can reject requests when too many calls are made quickly. The app should handle this gracefully.

Use:

- `asyncio.Semaphore` to limit parallel calls
- Retry failed requests
- Exponential backoff
- Clear error messages

Example retry delays:

```text
Attempt 1: wait 1 second
Attempt 2: wait 2 seconds
Attempt 3: wait 4 seconds
```

## Reliable JSON Response Strategy

AI models can sometimes return extra text around JSON. The project should reduce that risk with strong prompting and validation.

Prompt rules:

```text
Return only valid JSON.
Do not wrap the response in markdown.
Do not include explanations.
Use this exact schema.
If a value is missing, use "Not specified".
```

Validation rules:

- Load response with `json.loads()`
- Validate with Pydantic
- If validation fails, show the error clearly
- Optional: send the invalid response back to the model and ask it to repair the JSON

## Example Prompt

```text
You are an enterprise data extraction assistant.

Extract structured information from the text below.

Return only valid JSON.
Do not include markdown.
Do not include explanations.

Schema:
{
  "customer_name": "string or null",
  "issue_type": "Billing | Technical | Account | Other",
  "priority": "Low | Medium | High",
  "summary": "short summary",
  "sentiment": "Positive | Neutral | Negative",
  "action_items": [
    {
      "task": "string",
      "owner": "string",
      "deadline": "string"
    }
  ]
}

Text:
{user_text}
```

## Required Libraries

```text
boto3
python-dotenv
pydantic
```

Optional:

```text
rich
pytest
```

Install:

```bash
pip3 install -r requirements.txt
```

## Suggested `requirements.txt`

```text
boto3
python-dotenv
pydantic
rich
pytest
```

## Development Steps

### Step 1: Create The Schema

Start with Pydantic models in `schemas.py`.

Define:

- Customer information
- Issue type
- Priority
- Summary
- Sentiment
- Action items

### Step 2: Create The Prompt

Write a strict extraction prompt in `prompts/extraction_prompt.txt`.

Make sure it tells the model to return only JSON.

### Step 3: Connect Bedrock

Use `boto3` to call Bedrock Runtime.

The Bedrock client should stay inside `bedrock_client.py`.

### Step 4: Parse The Response

Use:

```python
json.loads(model_response)
```

Then validate:

```python
ExtractedRecord.model_validate(parsed_json)
```

### Step 5: Add Async Processing

Use `asyncio` to process many records.

Recommended pattern:

```python
asyncio.gather(*tasks)
```

Use a semaphore to avoid too many API calls at once.

### Step 6: Add Error Handling

Handle:

- Invalid JSON
- Missing fields
- API timeout
- Rate limit errors
- Empty input

### Step 7: Add Tests

Test:

- Valid JSON parsing
- Invalid JSON handling
- Pydantic validation
- Prompt formatting

## Success Criteria

The project is complete when:

- It accepts unformatted text input
- It sends the input to Bedrock
- It receives model output
- It parses valid JSON
- It validates the result with Pydantic
- It handles multiple records asynchronously
- It handles API errors and rate limits
- It produces a clean enterprise-style JSON result

## Stretch Goals

Optional improvements:

- Process a `.txt` or `.csv` file containing many conversations
- Save output to `output.json`
- Add a JSON repair step
- Add a small FastAPI endpoint
- Add CLI options for input and output files
- Add logging for failed records

## Final Deliverable

A working Automated Data Extractor that converts messy text into validated structured JSON objects.

The main learning outcome is understanding how to combine:

- Official API SDKs
- Async request handling
- Rate limit control
- Prompt engineering
- JSON parsing
- Pydantic schema validation
