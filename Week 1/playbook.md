# Prompt Engineering Playbook

## 1. Project Summary

This CLI app (`project.py`) accepts raw text from the user and runs it through a **parameterized prompt template** for one of three tasks:

1. **Summarization** — short bullet-point summary
2. **Sentiment Analysis** — label, reason, and confidence
3. **Action Item Extraction** — markdown table of tasks

The app sends the filled prompt to **AWS Bedrock** (Nemotron model) and prints the response. Temperature and top-p can be adjusted per run.

---

## 2. Prompt Design Strategy

| Task | Strategy |
| --- | --- |
| Summarization | Clear role, bullet output, rules against hallucination |
| Sentiment | Fixed output format so results are easy to read |
| Action items | Table format + explicit rules for missing owner/deadline |

All templates use `{user_text}` as the only variable — the user's input is injected at runtime.

---

## 3. Prompt Iterations

### Summarization

#### Iteration 1

**Prompt:** “Summarize this text.”

**Result:** Long paragraph, sometimes added details not in the source.

**Issue:** Too vague; model was creative.

**Improvement:** Added bullet rules and “do not add information not in the text.”

#### Iteration 2 (Final)

**Prompt:** Role + 3–5 bullets + rules (see `PROMPT_TEMPLATES["1"]` in `project.py`).

**Result:** Focused bullets, closer to source meaning.

**Issue:** Occasionally more than 5 bullets.

**Improvement:** Default `temperature=0.3` for steadier output.

---

### Sentiment Analysis

#### Iteration 1

**Prompt:** “What is the sentiment?”

**Result:** Long essay-style answers.

**Issue:** Hard to parse; inconsistent labels.

**Improvement:** Required exact format: `Sentiment:`, `Reason:`, `Confidence:`.

#### Iteration 2 (Final)

**Prompt:** Fixed format template in `project.py`.

**Result:** One label + short reason.

**Issue:** Sometimes multiple sentiments mentioned.

**Improvement:** `temperature=0.1` for consistent classification.

---

### Action Item Extraction

#### Iteration 1

**Prompt:** “List all tasks.”

**Result:** Invented owners and deadlines.

**Issue:** Hallucinated metadata.

**Improvement:** Markdown table + “Not specified” rule + only extract clear tasks.

#### Iteration 2 (Final)

**Prompt:** Table columns + strict rules in `project.py`.

**Result:** Cleaner tables; fewer invented fields.

**Issue:** Misses implied tasks sometimes.

**Improvement:** `temperature=0.2`; keep input explicit in meetings/notes.

---

## 4. Parameter Experiments

| Task | Temperature tried | Top-p | Observation |
| --- | ---: | ---: | --- |
| Summarization | 0.7 | 0.9 | More varied wording; less consistent bullets |
| Summarization | **0.3** | **0.9** | **Best balance — used as default** |
| Sentiment | 0.5 | 0.9 | Occasionally mixed labels |
| Sentiment | **0.1** | **0.9** | **Most consistent — used as default** |
| Action items | 0.6 | 0.9 | Extra tasks invented |
| Action items | **0.2** | **0.9** | **More faithful extraction — used as default** |

**Takeaway:** Lower temperature works better for factual tasks (sentiment, extraction). Slightly higher (0.3) is fine for summarization.

---

## 5. Final Prompts

Final prompts live in `project.py` under `PROMPT_TEMPLATES` for tasks 1, 2, and 3.

Default parameters in `TASK_DEFAULTS`:

| Task | Temperature | Top-p |
| --- | ---: | ---: |
| Summarization | 0.3 | 0.9 |
| Sentiment Analysis | 0.1 | 0.9 |
| Action Item Extraction | 0.2 | 0.9 |

---

## 6. Key Learnings

- **Specific prompts beat vague ones** — format and rules matter more than length.
- **Low temperature** reduces hallucination for sentiment and action items.
- **Parameterized templates** (`{user_text}`) keep one codebase for all three tasks.
- **Document every change** in this playbook so you can explain what improved results.

---

## 7. How to Run

```bash
cd "Week 1"
pip install -r requirements.txt
# Copy .env_samples to .env and fill in AWS values
python project.py
```

**Input tip:** After pasting long text, type `END` on its own line. Do not use a blank line — pasted articles often contain empty lines between paragraphs.

---

## 8. Parameter Lab (`params_lab.py`)

Run experiments to see how **temperature** and **top_p** change outputs:

```bash
python3 params_lab.py
```

Scenarios included:

| # | What you learn |
| --- | --- |
| 1 | Temperature sweep (0.0 → 1.0) |
| 2 | Top-p sweep (0.5 → 1.0) |
| 3 | Summarization: good vs bad params |
| 4 | Sentiment: good vs bad params |
| 5 | Action items: good vs bad params |
| 6 | Creative slogans: when high temp helps |
| 7 | Four extreme combinations |
| 8 | Same prompt twice — stability vs randomness |

Record what you observe in **Section 4. Parameter Experiments** above.
