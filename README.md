# Week 1: Foundations of Generative AI & Prompt Engineering

## Project: Prompt Engineering Playbook & CLI Interface

This project is designed for beginners who are learning how Generative AI applications work. You will build a simple Python command-line application that accepts raw text from a user and uses AWS Bedrock with prompt templates to perform three tasks:

1. Summarization
2. Sentiment Analysis
3. Action Item Extraction

You will also create a `playbook.md` file to document your prompt experiments, parameter changes, mistakes, improvements, and final prompts.

The main goal is not just to call an AI model. The goal is to understand how better prompts and model parameters can produce better outputs.

---

## Learning Objectives

By completing this project, you should understand:

- What Generative AI and Large Language Models are
- Basic ideas behind Transformer architecture
- What tokenization means
- Why prompts affect model output
- How `temperature` changes creativity and consistency
- How `top_p` controls response diversity
- How to use AWS Bedrock from a Python application
- How to write reusable prompt templates
- How to build a small Python CLI application
- How to document prompt engineering experiments

---

## Beginner Concepts

### Generative AI

Generative AI creates new content such as text, images, code, or audio. In this project, we focus on text generation.

### Large Language Model

A Large Language Model, or LLM, is trained on large amounts of text and generates responses based on the input prompt.

Common LLM tasks include summarization, classification, extraction, rewriting, and question answering.

### AWS Bedrock

AWS Bedrock is a managed AWS service that gives access to foundation models through an API. In this project, Bedrock is the AI provider.

Your Python app will send the final prompt to AWS Bedrock and receive the generated response.


### Transformer Architecture

Modern LLMs are based on Transformer architecture. You do not need to build a Transformer in this project, but you should understand these basic parts:

- Tokens: small pieces of text
- Embeddings: numeric meaning of tokens
- Attention: helps the model focus on important parts of the input
- Layers: repeated processing blocks that help the model understand context

### Tokenization

LLMs break text into tokens before processing it.

Example:

```text
I love Generative AI!
```

May become:

```text
["I", " love", " Gener", "ative", " AI", "!"]
```

Tokenization matters because models have input and output limits.

### Temperature

`temperature` controls randomness.

| Value | Behavior | Best For |
| --- | --- | --- |
| `0.0 - 0.3` | Focused and consistent | Summaries, sentiment, extraction |
| `0.4 - 0.7` | Balanced | Rewriting, explanation |
| `0.8 - 1.0` | Creative and varied | Brainstorming, creative writing |

For this project, use low temperature for better accuracy.

### Top-p

`top_p` controls how many possible words the model considers while generating output.

| Value | Behavior |
| --- | --- |
| `0.8 - 0.9` | More focused |
| `0.9 - 1.0` | More flexible |

For this project, `top_p = 0.9` is a good default.

---

## What You Need To Build

Build a Python CLI app that:

- Shows a menu with three AI tasks
- Accepts raw text from the user
- Loads the correct prompt template
- Inserts the user text into the prompt
- Sends the prompt to AWS Bedrock
- Allows configuration of `temperature` and `top_p`
- Prints the result clearly in the terminal

---

## Required Tasks

### 1. Summarization

The app should convert long text into a short, clear summary.

Expected output:

```text
- Main point 1
- Main point 2
- Main point 3
```

Good summary behavior:

- Keeps the main meaning
- Removes unnecessary details
- Does not add new information
- Uses simple language

### 2. Sentiment Analysis

The app should classify the emotion or tone of the text.

Expected output:

```text
Sentiment: Positive / Negative / Neutral
Reason: Short explanation
Confidence: Low / Medium / High
```

Good sentiment behavior:

- Gives only one sentiment label
- Explains the reason briefly
- Does not over-explain

### 3. Action Item Extraction

The app should extract tasks from meeting notes, emails, or messages.

Expected output:

```markdown
| Action Item | Owner | Deadline |
| --- | --- | --- |
| Prepare report | Priya | Friday |
```

Good extraction behavior:

- Extracts only real tasks from the input
- Does not invent owners or deadlines
- Uses `Not specified` when information is missing

---

## Recommended Project Structure

```text
week-1-prompt-engineering/
│
├── README.md
├── main.py
├── requirements.txt
├── .env.example
├── playbook.md
│
├── src/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── llm_client.py
│   └── prompt_loader.py
│
├── prompts/
│   ├── summarization_prompt.txt
│   ├── sentiment_prompt.txt
│   └── action_items_prompt.txt
│
└── examples/
    ├── sample_input.txt
    └── sample_outputs.md
```

### File Responsibilities

| File | Purpose |
| --- | --- |
| `main.py` | Starts the app |
| `src/cli.py` | Handles menu, user input, and terminal output |
| `src/config.py` | Stores AWS region, Bedrock model ID, and default parameters |
| `src/llm_client.py` | Calls AWS Bedrock Runtime |
| `src/prompt_loader.py` | Loads prompt templates from files |
| `prompts/` | Stores reusable prompt templates |
| `examples/` | Stores sample inputs and outputs |
| `playbook.md` | Documents prompt experiments |
| `.env.example` | Shows required environment variables |

---

## Simple Architecture

```text
User
 |
 v
Python CLI
 |
 v
Task Selection
 |
 v
Prompt Template
 |
 v
Bedrock Client
 |
 v
AI Response
 |
 v
Terminal Output
```

The CLI should not contain all the logic in one file. Keep the project simple, but separate responsibilities clearly.

### Bedrock Responsibility

Only `src/llm_client.py` should directly communicate with AWS Bedrock. Other files should not call Bedrock directly.

This keeps the project easy to understand:

- `cli.py` handles the user experience
- `prompt_loader.py` handles prompt files
- `config.py` handles settings
- `llm_client.py` handles AWS Bedrock

Inside `llm_client.py`, use `boto3` to create a Bedrock Runtime client. The exact request body can depend on the model selected by the mentor, so keep this file isolated and easy to update.

---

## How The CLI Should Work

Example terminal flow:

```text
Welcome to the Prompt Engineering CLI

Choose a task:
1. Summarization
2. Sentiment Analysis
3. Action Item Extraction
4. Exit

Enter your choice: 1

Paste your text:
> The product team discussed the launch plan...

Temperature [default: 0.3]:
Top-p [default: 0.9]:

Processing...

Result:
- The product team discussed the launch plan.
- Key responsibilities were assigned.
- Final assets need to be completed before launch.
```

---

## Prompt Templates

Store each prompt in a separate file inside the `prompts/` folder. Use `{user_text}` as the placeholder for user input.

### `prompts/summarization_prompt.txt`

```text
You are a helpful assistant that summarizes text clearly.

Task:
Summarize the text in 3-5 bullet points.

Rules:
- Keep the summary concise.
- Preserve the main ideas.
- Do not add information that is not in the text.
- Use simple language.

Text:
{user_text}
```

### `prompts/sentiment_prompt.txt`

```text
You are a sentiment analysis assistant.

Task:
Analyze the sentiment of the text.

Return the output in this exact format:
Sentiment: Positive, Negative, or Neutral
Reason: One short sentence
Confidence: Low, Medium, or High

Text:
{user_text}
```

### `prompts/action_items_prompt.txt`

```text
You are an assistant that extracts action items from text.

Task:
Extract all action items from the text.

Return the output as a markdown table with these columns:
Action Item | Owner | Deadline

Rules:
- Only extract tasks that are clearly mentioned.
- If owner is missing, write "Not specified".
- If deadline is missing, write "Not specified".
- Do not create action items that are not present in the text.

Text:
{user_text}
```

---

## Setup Instructions

### 1. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 2. Install Dependencies

Create `requirements.txt`:

```text
python-dotenv
boto3
rich
```

Install:

```bash
pip install -r requirements.txt
```

### 3. Create Environment File

Create `.env.example`:

```text
AWS_REGION=your_aws_region_here
BEDROCK_MODEL_ID=your_bedrock_model_id_here
AWS_PROFILE=optional_local_aws_profile_name
```

Then create your real `.env` file:

```text
AWS_REGION=ap-south-1
BEDROCK_MODEL_ID=model_id_provided_by_mentor
AWS_PROFILE=your_local_aws_profile_name
```

Never commit your real `.env` file.

For local development, AWS credentials should come from your normal AWS setup, such as:

- AWS CLI profile
- Environment variables
- IAM role if running on AWS

Do not hardcode AWS access keys or secret keys in Python files.

Beginner note: the `.env` file should store simple project settings like region and model ID. AWS credentials should be managed through AWS CLI, IAM roles, or environment variables outside the source code.

### 4. Check Bedrock Access

Before running the app, make sure:

- Your AWS account has Bedrock access enabled
- The selected model is available in your AWS region
- Your IAM user or role has permission to call Bedrock Runtime
- The model ID in `.env` matches the model provided by the mentor

### 5. Run The App

```bash
python main.py
```

---

## Recommended Parameters

| Task | Temperature | Top-p | Why |
| --- | ---: | ---: | --- |
| Summarization | `0.2 - 0.4` | `0.9` | Needs focused output |
| Sentiment Analysis | `0.0 - 0.2` | `0.8 - 1.0` | Needs consistent classification |
| Action Item Extraction | `0.0 - 0.3` | `0.9` | Needs accurate extraction |

High temperature can make the model creative, but this project needs accuracy and consistency.

---

## Prompt Engineering Playbook

Create `playbook.md` to document your experiments.

Your playbook should include:

- Project summary
- Prompt design strategy
- Prompt iterations
- Parameter experiments
- Final prompts
- Key learnings

Use this structure:

```markdown
# Prompt Engineering Playbook

## 1. Project Summary

Explain what the CLI app does.

## 2. Prompt Design Strategy

Explain how you designed prompts for each task.

## 3. Prompt Iterations

### Summarization

#### Iteration 1

Prompt:

Result:

Issue:

Improvement:

#### Iteration 2

Prompt:

Result:

Issue:

Improvement:

### Sentiment Analysis

Document at least 2 iterations.

### Action Item Extraction

Document at least 2 iterations.

## 4. Parameter Experiments

| Task | Temperature | Top-p | Result Quality | Notes |
| --- | ---: | ---: | --- | --- |

## 5. Final Prompts

Add the final prompt for each task.

## 6. Key Learnings

Write what you learned in your own words.
```

Minimum playbook requirement:

- 2 prompt iterations for each task
- 3 parameter experiments
- Final prompt for each task
- Key learnings in your own words

---

## Example Input And Outputs

### Input

```text
During the weekly product meeting, Priya agreed to prepare the user feedback report by Friday. Rahul will check the payment issue before tomorrow evening. The team also discussed improving onboarding but did not assign anyone to that task.
```

### Summarization Output

```text
- Priya will prepare the user feedback report by Friday.
- Rahul will check the payment issue before tomorrow evening.
- The team discussed onboarding improvements, but no owner was assigned.
```

### Sentiment Output

```text
Sentiment: Neutral
Reason: The text is factual and task-focused.
Confidence: High
```

### Action Item Output

```markdown
| Action Item | Owner | Deadline |
| --- | --- | --- |
| Prepare the user feedback report | Priya | Friday |
| Check the payment issue | Rahul | Tomorrow evening |
```

---

## Success Criteria

Your project is successful when:

- `python main.py` starts the CLI
- The user can select all three tasks
- The app accepts raw text input
- Prompt templates are loaded from the `prompts/` folder
- `temperature` and `top_p` can be changed
- AI responses are displayed clearly
- Empty input and invalid menu choices are handled
- AWS region and Bedrock model ID are loaded from `.env`
- AWS credentials are not hardcoded
- `playbook.md` contains prompt iterations and learnings

---

---

## Common Mistakes To Avoid

- Writing one generic prompt for all tasks
- Using high temperature for sentiment analysis
- Hardcoding AWS access keys or secret keys
- Skipping prompt iteration documentation
- Not testing unclear or messy input
- Inventing action items that were not in the text
- Mixing all code into one large file
- Producing long summaries when a short summary is requested

---

## Stretch Goals

After completing the required version, you can try:

- Add `argparse` command-line arguments
- Add colored output using `rich`
- Save results to a file
- Add JSON output mode
- Read input from a `.txt` file
- Add a token counter
- Add unit tests for prompt loading

---

## Final Submission Checklist

Submit a complete project folder containing:

```text
README.md
main.py
requirements.txt
.env.example
playbook.md
src/
prompts/
examples/
```

Before submission, test all three tasks and make sure the playbook explains what changed between prompt versions.
