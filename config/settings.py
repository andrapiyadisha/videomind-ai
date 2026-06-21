import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

LLM_MODEL = "llama-3.1-8b-instant"

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

VECTOR_DB_PATH = "data/vectorstore"
TRANSCRIPT_PATH = "data/transcripts"