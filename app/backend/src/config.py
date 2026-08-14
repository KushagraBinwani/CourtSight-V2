from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# =========================
# Paths
# =========================

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent.parent
STORAGE_DIR = PROJECT_ROOT / "storage"

PDF_DIR = STORAGE_DIR / "pdf"
METADATA_DIR = STORAGE_DIR / "metadata"
PROCESSED_DIR = STORAGE_DIR / "processed"
EMBEDDINGS_DIR = STORAGE_DIR / "embeddings"

# Backend runtime artifacts
BACKEND_STORAGE_DIR = BACKEND_DIR / "storage"
INDEX_DIR = BACKEND_STORAGE_DIR / "index"

# =========================
# API Keys
# =========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# Models
# =========================

LLM_MODEL = "gemini-3.6-flash"

# =========================
# Chunking
# =========================

CHUNK_SIZE = 450
CHUNK_OVERLAP = 75
SENTENCE_TOLERANCE = 30

# =========================
# Embeddings
# =========================

EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_BATCH_SIZE = 256