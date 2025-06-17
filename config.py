
PDF_PATH = "academic_manual.pdf"
DB_PERSIST_DIRECTORY = "./chroma_db"
MODELS_CACHE_DIR = "./models" # Directory to cache Hugging Face embedding models

#  Embedding Model Settings
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Text Splitting Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# LLM Settings for Groq API
USE_LLM_API = True
LLM_API_PROVIDER = "groq"
LLM_API_MODEL_NAME = "llama3-8b-8192"

# Retrieval Settings
TOP_K_RETRIEVAL = 5


