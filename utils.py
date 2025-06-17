import os

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq


from dotenv import load_dotenv

from config import (
    EMBEDDING_MODEL_NAME, DB_PERSIST_DIRECTORY, MODELS_CACHE_DIR,
    LLM_API_PROVIDER, LLM_API_MODEL_NAME, USE_LLM_API
)

load_dotenv()


def get_embedding_model():
    """Initializes and returns the HuggingFaceEmbeddings model."""
    print(f"Loading embedding model: {EMBEDDING_MODEL_NAME}")
    hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")  # Get HF token for embedding model if needed

    # Pass model_kwargs including token directly to HuggingFaceEmbeddings
    # If the model requires a token, it will be used.
    model_kwargs = {}
    if hf_token:
        model_kwargs['token'] = hf_token

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        cache_folder=MODELS_CACHE_DIR,
        model_kwargs=model_kwargs
    )


def get_vector_store():
    """Initializes and returns the Chroma vector store."""
    print(f"Loading vector store from: {DB_PERSIST_DIRECTORY}")
    embeddings = get_embedding_model()
    return Chroma(
        persist_directory=DB_PERSIST_DIRECTORY,
        embedding_function=embeddings
    )


def get_api_llm():
    """Initializes and returns an LLM from an API provider (Groq)."""
    print(f"Initializing LLM from API: {LLM_API_PROVIDER} - Model: {LLM_API_MODEL_NAME}")
    if LLM_API_PROVIDER == "groq":
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set.")
        return ChatGroq(temperature=0.1, groq_api_key=groq_api_key, model_name=LLM_API_MODEL_NAME, max_tokens=8192)
    else:
        # This case should ideally not be reached if USE_LLM_API is True and LLM_API_PROVIDER is "groq"
        # as set in config.py, but kept for robustness.
        raise ValueError(f"Unsupported LLM API provider or USE_LLM_API is False: {LLM_API_PROVIDER}")



def get_llm_for_rag():
    return get_api_llm()

