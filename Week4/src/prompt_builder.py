def build_prompt(question, context, chat_history=None):
    """
    Build the LLM prompt.

    chat_history: optional list of {"role": "user"|"assistant", "content": str}
    """
    history_text = ""
    if chat_history:
        for msg in chat_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"

    prompt = f"""
You are a helpful assistant answering questions based ONLY on the provided context.

Read the context carefully. If the answer to the question is found in the context, provide a clear and concise answer.
If the answer is NOT found in the context, you must reply EXACTLY with:
"I could not find that information in the uploaded documents."

<Context>
{context}
</Context>
"""

    if history_text:
        prompt += f"""
<ConversationHistory>
{history_text}
</ConversationHistory>
"""

    prompt += f"""
<Question>
{question}
</Question>

Answer:
"""

    return prompt