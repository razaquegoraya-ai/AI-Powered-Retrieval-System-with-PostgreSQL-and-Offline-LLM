from langchain.llms import CTransformers
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from config import MODEL_CONFIG, MODEL_DIR
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def load_llm():
    """
    Load the offline LLM model using CTransformers with caching.
    """
    llm = CTransformers(
        model=MODEL_CONFIG['model_name'],
        model_type=MODEL_CONFIG['model_type'],
        max_new_tokens=MODEL_CONFIG['max_new_tokens'],
        temperature=MODEL_CONFIG['temperature'],
        top_p=MODEL_CONFIG['top_p'],
        callbacks=[StreamingStdOutCallbackHandler()],
        config={
            'context_length': MODEL_CONFIG.get('context_length', 1024),
            'gpu_layers': MODEL_CONFIG.get('gpu_layers', 0),
            'threads': os.cpu_count() or 4,  # Use available CPU threads
            'batch_size': 1  # Optimize for single queries
        }
    )
    return llm

@lru_cache(maxsize=1)
def load_embeddings():
    """
    Load the embedding model with caching.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True},
        cache_folder=MODEL_DIR
    )
    return embeddings

def download_model():
    """
    Download the model if it doesn't exist locally.
    """
    print(f"Model will be downloaded to {MODEL_DIR} when first used.")