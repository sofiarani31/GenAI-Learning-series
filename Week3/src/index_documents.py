from src.ingestion.parser import load_documents
from src.ingestion.text_cleaner import clean_text
from src.ingestion.chunker import create_chunks
from src.embeddings.embedding_model import generate_embedding
from src.vectordb.pinecone_client import create_index


def index_documents(folder_path):

    index = create_index()

    documents = load_documents(folder_path)

    total_chunks = 0

    for doc in documents:

        cleaned_text = clean_text(
            doc["text"]
        )

        chunks = create_chunks(
            cleaned_text,
            doc["filename"]
        )

        vectors = []

        for chunk in chunks:

            embedding = generate_embedding(
                chunk["text"]
            )

            vectors.append(
                (
                    chunk["id"],
                    embedding.tolist(),
                    chunk["metadata"]
                    | {"text": chunk["text"]}
                )
            )

        if vectors:
            index.upsert(vectors=vectors)

        total_chunks += len(chunks)

    return total_chunks