from src.vector_store import get_index
from src.config import TOP_K

def retrieve_chunks(
    query_embedding,
    top_k=TOP_K,
    filter_document=None
):
    """
    Retrieve similar chunks from Pinecone.

    filter_document: optional document name to restrict results to a
    single source file.
    """
    index = get_index()

    filter_dict = None
    if filter_document:
        filter_dict = {"document": {"$eq": filter_document}}

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter=filter_dict
    )

    return results.get("matches", [])