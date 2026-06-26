from pypdf import PdfReader
from pypdf.errors import PdfReadError, PdfStreamError


def extract_text(file_path):
    """
    Extract text from a PDF file, tracking page numbers.

    Returns:
        list of {"page": int, "text": str}

    Raises:
        ValueError — for corrupt, non-PDF, or scanned/image-only files.
    """
    try:
        reader = PdfReader(file_path, strict=False)
    except (PdfReadError, PdfStreamError) as e:
        raise ValueError(f"Could not read PDF: {e}")
    except Exception as e:
        raise ValueError(f"Unexpected error opening PDF: {e}")

    pages = []

    try:
        page_list = list(reader.pages)
    except (PdfStreamError, PdfReadError, Exception) as e:
        raise ValueError(f"Could not read PDF pages: {e}")

    for i, page in enumerate(page_list):
        try:
            page_text = page.extract_text() or ""
        except Exception:
            page_text = ""

        if page_text.strip():
            pages.append({
                "page": i + 1,
                "text": page_text.strip()
            })

    if not pages:
        raise ValueError(
            "No extractable text found. "
            "The PDF may be scanned or image-only."
        )

    return pages