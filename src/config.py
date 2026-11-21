import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
RERANK_DEVICE = os.getenv("RERANK_DEVICE", "cuda")

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION = "german_rag"

# Models
EMBED_MODEL = "qwen3-embedding:0.6b"
EMBED_DIM = 1024
LLM_MODEL = "qwen3.5:4b"
RERANK_MODEL = "BAAI/bge-reranker-v2-m3"
TOKENIZER_MODEL = "Qwen/Qwen3.5-4B"

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Retrieval
TOP_K = 5
RERANK_TOP_N = 4
SCORE_THRESHOLD = 0.35
MAX_CONTEXT_TOKENS = 1500

# Agent
MAX_RETRIES = 2

# Messages
NO_INFO = "Dazu habe ich keine Informationen in meinen Dokumenten."
TOKEN_OVER = "Token-Limit überschritten: der Kontext ist zu groß für das Budget."