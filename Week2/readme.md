# Enterprise AI Data Extraction Pipeline

## Overview
This project is an enterprise-style AI-powered data extraction pipeline built using AWS Bedrock, Python, and Pydantic. 

The application accepts unstructured customer conversations, support tickets, incident reports, or logs, then uses a Large Language Model (LLM) to extract meaningful information and convert it into validated structured JSON. 

The project demonstrates practical concepts used in production AI systems, including asynchronous processing, rate limiting, prompt engineering, JSON parsing, and schema validation.

## Features
- **Generative AI Parsing**: Uses AWS Bedrock (via `boto3`) to extract specific action items, sentiment, and summaries from raw text.
- **Strict Data Validation**: Enforces JSON schemas using `Pydantic` to ensure reliable backend integration and prevent hallucinations.
- **Enterprise Concurrency**: Utilizes Python's `asyncio.gather()` to process massive batches of customer logs simultaneously rather than waiting sequentially.
- **Built-in Rate Limiting**: Uses asynchronous semaphores and automatic exponential backoff to handle AWS API throttling seamlessly.
- **Dual Interfaces**: 
  - **Robust CLI**: A fully functional Command Line Interface (`main.py`) for automated backend processing.
  - **Interactive Streamlit Web UI (`app.py`)**: 
    - **Single Record Mode**: Paste a single conversation into a text box to instantly extract data.
    - **Massive Batch Uploads**: Drag and drop multiple `.csv` or `.txt` files at once. The app will automatically slice them into distinct records and process them concurrently.
    - **Data Table Previews**: Automatically renders extracted JSON results into a beautiful, sortable data table in your browser.
    - **One-Click Export**: Easily download all successfully parsed records as a clean `results.json` file.

## Learning Outcomes
This project helped me understand:
- AWS Bedrock integration using `boto3`
- Prompt engineering for structured output
- JSON parsing and validation
- Pydantic schema enforcement
- Asynchronous programming with `asyncio`
- Concurrent task execution using `asyncio.gather()`
- Rate limiting with semaphores
- Retry mechanisms with exponential backoff
- Enterprise-style AI application architecture
- Interactive Streamlit Web UI
