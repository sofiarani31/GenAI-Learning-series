from pathlib import Path
from pypdf import PdfReader
from docx import Document
from src.utils.logger import get_logger

logger = get_logger(__name__)

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def read_docx(file_path):
    doc = Document(file_path)

    return "\n".join(
        para.text for para in doc.paragraphs
    )


def load_documents(folder_path):

    documents = []

    for file in Path(folder_path).iterdir():

        try:

            if file.suffix == ".txt":
                text = read_txt(file)

            elif file.suffix == ".pdf":
                text = read_pdf(file)

            elif file.suffix == ".docx":
                text = read_docx(file)

            else:
                logger.info(f"Skipping unsupported file type: {file.name}")
                continue

            documents.append(
                {
                    "filename": file.name,
                    "text": text
                }
            )

        except Exception as e:
            logger.error(f"Error reading {file.name}: {str(e)}")

    return documents