from src.config import CHUNK_SIZE, CHUNK_OVERLAP

def create_chunks(pages):
    """
    Split pages into overlapping fixed-size chunks.

    Args:
        pages: list of {"page": int, "text": str}
               returned by pdf_loader.extract_text()

    Returns:
        list of {"text": str, "page": int}
    """
    chunks = []

    for page in pages:
        text = page["text"]
        page_num = page["page"]
        start = 0

        while start < len(text):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_num
                })

            start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks