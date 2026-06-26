from pinecone import Pinecone, ServerlessSpec

from src.config import (
    PINECONE_API_KEY,
    INDEX_NAME
)

pc = Pinecone(
    api_key=PINECONE_API_KEY
)


def create_index():

    existing = pc.list_indexes().names()

    if INDEX_NAME not in existing:

        pc.create_index(
            name=INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc.Index(INDEX_NAME)


def clear_index():
    existing = pc.list_indexes().names()
    if INDEX_NAME in existing:
        pc.delete_index(INDEX_NAME)