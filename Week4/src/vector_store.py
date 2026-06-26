from pinecone import Pinecone, ServerlessSpec

from src.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX,
    PINECONE_CLOUD,
    PINECONE_REGION
)

_index = None

def get_index():
    global _index

    if _index is not None:
        return _index

    pc = Pinecone(api_key=PINECONE_API_KEY)

    existing = [i.name for i in pc.list_indexes()]
    if PINECONE_INDEX not in existing:
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=PINECONE_CLOUD,
                region=PINECONE_REGION
            )
        )

    _index = pc.Index(PINECONE_INDEX)
    return _index


def store_chunks(chunks, embeddings, document_name):
    """
    Store document chunks in Pinecone.

    chunks: list of {"text": str, "page": int}
    embeddings: list of vectors
    """
    index = get_index()
    vectors = []

    for chunk_id, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):
        vectors.append(
            {
                "id": f"{document_name}_{chunk_id}",
                "values": embedding,
                "metadata": {
                    "document": document_name,
                    "chunk_id": chunk_id,
                    "page": chunk["page"],
                    "text": chunk["text"]
                }
            }
        )

    if vectors:
        index.upsert(vectors=vectors)


def delete_by_document(document_name):
    """
    Delete all vectors belonging to document_name from Pinecone.
    Called before re-indexing an already-uploaded file.
    """
    index = get_index()
    index.delete(filter={"document": {"$eq": document_name}})