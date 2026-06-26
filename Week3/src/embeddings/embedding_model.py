from sentence_transformers import (
    SentenceTransformer
)

from src.config import EMBEDDING_MODEL

model = SentenceTransformer(
    EMBEDDING_MODEL
)


def generate_embedding(text):

    return model.encode(
        text,
        convert_to_numpy=True
    )


def generate_embeddings(texts):

    return model.encode(
        texts,
        convert_to_numpy=True
    )