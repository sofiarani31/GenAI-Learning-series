from src.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

def create_chunks(text, filename):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk_words = []
    chunk_index = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        words = para.split()
        
        # If adding this paragraph exceeds CHUNK_SIZE and we already have words
        if len(current_chunk_words) + len(words) > CHUNK_SIZE and current_chunk_words:
            # Save the current chunk
            chunk_text = " ".join(current_chunk_words)
            chunks.append({
                "id": f"{filename}_{chunk_index}",
                "text": chunk_text,
                "metadata": {
                    "source_file": filename,
                    "chunk_index": chunk_index
                }
            })
            chunk_index += 1
            
            # Start new chunk with overlap from the previous one
            overlap = current_chunk_words[-CHUNK_OVERLAP:] if CHUNK_OVERLAP > 0 else []
            current_chunk_words = overlap
            
        # Add the current paragraph's words
        current_chunk_words.extend(words)

    # Add the last chunk if anything is left
    if current_chunk_words:
        chunk_text = " ".join(current_chunk_words)
        chunks.append({
            "id": f"{filename}_{chunk_index}",
            "text": chunk_text,
            "metadata": {
                "source_file": filename,
                "chunk_index": chunk_index
            }
        })

    return chunks