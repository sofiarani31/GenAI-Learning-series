from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL

_model = None


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_embedding(text):
    return get_model().encode(text).tolist()


def get_embeddings(texts):
    return get_model().encode(texts).tolist()