from src.embeddings.embedding_model import generate_embedding
from src.vectordb.pinecone_client import create_index

from src.config import TOP_K


def semantic_search(
    query,
    top_k=TOP_K
):

    index = create_index()

    query_vector = generate_embedding(
        query
    )

    results = index.query(
        vector=query_vector.tolist(),
        top_k=top_k,
        include_metadata=True
    )

    return results.matches