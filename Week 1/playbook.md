# Prompt Engineering Playbook

## 1. Project Summary
Python command-line application uses AWS Bedrock and prompt engineering techniques to perform three Generative AI tasks:

Text Summarization
Sentiment Analysis
Action Item Extraction

The user selects a task from the CLI menu, enters raw text, and the application loads the appropriate prompt template. The prompt is then sent to an AI model through AWS Bedrock, and the generated response is displayed in the terminal.

The application also separates responsibilities into different modules such as CLI handling, prompt loading, configuration management, and Bedrock communication to keep the code clean and maintainable.

## 2. Prompt Design Strategy

Different prompts were created for each task to get accurate and structured outputs.

For summarization, the prompt focused on generating short bullet points while preserving the main meaning.
For sentiment analysis, the prompt guided the model to identify the overall tone and return results in a fixed format.
For action item extraction, the prompt instructed the model to extract only clearly mentioned tasks and return them.

Additional rules and prompt iterations were added to improve clarity, consistency, and output quality.

## 3. Prompt Iterations

### Summarization

#### Iteration 1

Prompt: 
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

Result:
- The marketing team met on Tuesday to discuss the upcoming product launch.
- They are excited about the campaign strategy and design improvements from the UI team.
- Concerns were raised about a delayed backend API integration that could affect the launch timeline.
- Sarah will work with backend developers to fix the issues before Friday.
- John must finalize social media content and send it for approval by Wednesday evening.
- A follow-up review meeting is scheduled for next Monday to track progress.

Issue:
In prompt, i mentioned 3-5 bullet points, but in result it summarized to 6 
It seems like simple converted every text to bullet points

Improvement:


#### Iteration 2

Prompt:
You are a helpful assistant that summarizes text clearly.

Task:
Summarize the text in exact 5 bullet points.

Rules:
- Keep the summary concise.
- Preserve the main ideas.
- Do not add information that is not in the text.
- Use simple language.

Text:
{user_text}

Result:
- The marketing team met on Tuesday to discuss the upcoming product launch.
- The team is excited about the campaign strategy and the design improvements from the UI team.
- Concerns were raised about the delayed backend API integration, which could delay the launch.
- Sarah will work with backend developers to fix the issues before Friday.
- John must finalize social media content and get it approved by Wednesday evening.

Issue:
It missed the next meeting scheduled, by including "The team is excited about the campaign strategy and the design improvements from the UI team"

Improvement:

#### Iteration 3

Prompt:
Summarize the text into EXACTLY 5 bullet points.

Priority Rules:
- Prioritize decisions, action items, deadlines, risks, Decisions made, and upcoming meetings or plans or scheduled events.
- Avoid General opinions, Emotional reactions, and Repetitive details.
- If space is limited, avoid minor opinions.
- Preserve the original meaning.
- Do not add information that is not present in the text.
- Use simple and concise language.

Output Format:
- One sentence per bullet point
- EXACTLY 5 bullet points

Text:
{user_text}

Result:
- Marketing team met Tuesday to discuss upcoming product launch.
- Concerns raised about delayed backend API integration affecting timeline.
- Sarah will coordinate with backend developers to resolve issues before Friday.
- John must finalize social media content and send for approval by Wednesday evening.
- Review meeting scheduled for next Monday to track progress.

Issue:
No issues, looks good.

Improvement:

### Sentiment Analysis

#### Iteration 1

Prompt:
You are a sentiment analysis assistant.

Task:
1. Analyze the sentiment of each sentence individually.
2. Determine the overall sentiment based on the majority sentiment across sentences.

Rules:
- Focus on the dominant emotional tone of each sentence.
- Use the majority sentiment to determine the final overall sentiment.
- If sentiments are evenly mixed, return Neutral.

Return the output in this exact format:
Sentiment: Positive, Negative, or Neutral
Reason: One short sentence
Confidence: Low, Medium, or High

Text:
{user_text}

Result:
Sentiment: Positive
Reason: The meeting focused on constructive progress and collaboration despite minor concerns.
Confidence: High

Issue:
Returns as positive since meeting focused on constructive progress and collaboration, but important thing to notice in meetings is pending tasks/ issues.

Improvement:

#### Iteration 2

Prompt:
You are a sentiment analysis assistant.

Task:
Analyze the sentiment of the text.

Return the output in this exact format:
Sentiment: Positive, Negative, or Neutral
Reason: One short sentence
Confidence: Low, Medium, or High

Text:
{user_text}

Result:
Sentiment: Neutral
Reason: The text presents both positive and negative elements without a clear overall leaning.
Confidence: Medium

Issue:
No issue.

Improvement:

### Action Item Extraction

#### Iteration 1
Prompt:
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

Result:
| Action Item                                      | Owner      | Deadline           |
|--------------------------------------------------|------------|--------------------|
| Coordinate with backend developers to resolve pending issues | Sarah      | Friday             |
| Finalize social media content and send to approval team | John       | Wednesday evening  |

Issue:
Action descriptions are still too long.
Future meeting was ignored.

Improvement:

#### Iteration 2

Prompt:
You are an assistant that extracts action items from meeting notes.

Task:
Extract all actionable tasks, follow-ups, and scheduled activities mentioned in the text.

Return the output as a markdown table with these columns:

| Action Item | Owner | Deadline |

Rules:
- Include assigned tasks, follow-up actions, and scheduled review activities.
- Keep action item descriptions concise (3-6 words if possible).
- Rewrite long sentences into short task phrases.
- If the owner is a group or team, use the team name.
- If owner is missing, write "Not specified".
- If deadline is missing, write "Not specified".
- Do not invent tasks or deadlines.

Text:
{user_text}

Result:
| Action Item                     | Owner             | Deadline       |
|---------------------------------|-------------------|----------------|
| Coordinate backend integration  | Sarah             | Friday         |
| Finalize social media content   | John              | Wednesday evening |
| Schedule review meeting         | Not specified     | Next Monday    |

Issue:
No issues, looks good.

Improvement:

## 4. Parameter Experiments

| Task                   | Temperature | Top-p | Result Quality | Notes                                                 |
| ---------------------- | ----------: | ----: | -------------- | ----------------------------------------------------- |
| Summarization          |         0.3 |   0.9 | Good           | Included most important points clearly.               |
| Summarization          |         0.4 |   0.9 | Moderate       | Output changed slightly in different runs.            |
| Summarization          |         0.4 |   0.9 | Poor           | Summary format became inconsistent.                   |
| Summarization          |         0.4 |   0.9 | Good           | Generated shorter and cleaner summary.                |
| Sentiment Analysis     |         0.3 |   0.9 | Moderate       | Mostly returned Neutral sentiment.                    |
| Sentiment Analysis     |         0.2 |   0.8 | Good           | More consistent sentiment output.                     |
| Sentiment Analysis     |         0.0 |   0.8 | Good           | Very stable and less random output.                   |
| Sentiment Analysis     |         0.2 |   0.4 | Moderate       | Lower diversity in responses.                         |
| Sentiment Analysis     |         0.2 |   0.8 | Good           | Improved prompt gave Positive sentiment.              |
| Sentiment Analysis     |         0.2 |   0.8 | Experimental   | Sentence-level analysis gave detailed reasoning.      |
| Action Item Extraction |         0.3 |   0.9 | Moderate       | Extracted tasks correctly but descriptions were long. |
| Action Item Extraction |         0.3 |   0.9 | Good           | Improved prompt gave shorter and clearer tasks.       |

## 5. Final Prompts
### Text Summarization:

Summarize the text into EXACTLY 5 bullet points.

Priority Rules:
- Prioritize decisions, action items, deadlines, risks, Decisions made, and upcoming meetings or plans or scheduled events.
- Avoid General opinions, Emotional reactions, and Repetitive details.
- If space is limited, avoid minor opinions.
- Preserve the original meaning.
- Do not add information that is not present in the text.
- Use simple and concise language.

Output Format:
- One sentence per bullet point
- EXACTLY 5 bullet points

Text:
{user_text}

### Sentiment Analysis:

You are a sentiment analysis assistant.

Task:
Analyze the sentiment of the text.

Return the output in this exact format:
Sentiment: Positive, Negative, or Neutral
Reason: One short sentence
Confidence: Low, Medium, or High

Text:
{user_text}

### Action Item Extraction:
You are an assistant that extracts action items from meeting notes.

Task:
Extract all actionable tasks, follow-ups, and scheduled activities mentioned in the text.

Return the output as a markdown table with these columns:

| Action Item | Owner | Deadline |

Rules:
- Include assigned tasks, follow-up actions, and scheduled review activities.
- Keep action item descriptions concise (3-6 words if possible).
- Rewrite long sentences into short task phrases.
- If the owner is a group or team, use the team name.
- If owner is missing, write "Not specified".
- If deadline is missing, write "Not specified".
- Do not invent tasks or deadlines.

Text:
{user_text}

## 6. Key Learnings

Learned how to structure a Python CLI project with separate responsibilities.
Learned how to use AWS Bedrock with Python using boto3.
Understood the effect of temperature and top_p on output quality and consistency.
Learned how prompt wording affects AI responses and need of clarity in instructions
Improving prompts through multiple iterations.
