import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma


from config import PDF_PATH, DB_PERSIST_DIRECTORY, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL_NAME, MODELS_CACHE_DIR
from utils import get_embedding_model

def ingest_data():
    """
    Loads PDF, splits it into chunks, generates embeddings, and stores them in ChromaDB.
    """
    # Ensure necessary directories exist before starting
    os.makedirs(MODELS_CACHE_DIR, exist_ok=True)
    os.makedirs(DB_PERSIST_DIRECTORY, exist_ok=True)

    if not os.path.exists(PDF_PATH):
        print(f"Error: PDF file not found at {PDF_PATH}. Please place your 'academic_manual.pdf' in the project root.")
        return

    print(f"Loading PDF from: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")

    print(f"Splitting documents into chunks (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} text chunks.")

    print(f"Initializing embedding model: {EMBEDDING_MODEL_NAME}")
    embeddings = get_embedding_model()

    print(f"Creating ChromaDB vector store at: {DB_PERSIST_DIRECTORY}")
    # This will create or load the vector store and automatically persist it
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=DB_PERSIST_DIRECTORY
    )

    print("Vector database built and persisted successfully!")

if __name__ == "__main__":
    ingest_data()