import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

PINECONE_CLOUD = os.getenv("PINECONE_CLOUD", "aws")
PINECONE_REGION = os.getenv("PINECONE_REGION", "us-east-1")

PINECONE_INDEX = "pdf-rag"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

GEMINI_MODEL = "gemini-2.5-flash"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K = 5