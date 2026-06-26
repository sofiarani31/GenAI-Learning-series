import traceback

import google.generativeai as genai

from src.config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL
)

from src.embeddings import get_embedding
from src.retriever import retrieve_chunks
from src.prompt_builder import build_prompt

genai.configure(api_key=GOOGLE_API_KEY)

SIMILARITY_THRESHOLD = 0.30

def generate_answer(question, chat_history=None):
    """
    Complete RAG workflow.
    """
    try:

        # Convert question to embedding
        query_embedding = get_embedding(question)

        # Retrieve chunks
        matches = retrieve_chunks(query_embedding)

        # Filter low-score chunks
        relevant_matches = [
            match
            for match in matches
            if match["score"] >= SIMILARITY_THRESHOLD
        ]

        if not relevant_matches:
            return (
                "I could not find relevant information in the uploaded documents.",
                []
            )

        # Build context
        context_parts = []

        for match in relevant_matches:
            metadata = match["metadata"]
            context_parts.append(
                f"Document: {metadata['document']}\n"
                f"Page: {metadata.get('page', 'N/A')}\n"
                f"Chunk ID: {metadata['chunk_id']}\n\n"
                f"{metadata['text']}"
            )

        context = "\n\n".join(context_parts)

        # Build prompt
        prompt = build_prompt(
            question=question,
            context=context,
            chat_history=chat_history
        )

        # Generate answer
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content(prompt)
        
        answer = response.text.strip()

        return (answer, relevant_matches)

    except Exception as e:
        traceback.print_exc()
        return (
            f"Error generating answer: {str(e)}",
            []
        )