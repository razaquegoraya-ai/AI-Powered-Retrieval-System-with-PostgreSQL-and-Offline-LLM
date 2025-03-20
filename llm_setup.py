from langchain.llms import CTransformers
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from config import MODEL_CONFIG, MODEL_DIR
import os

def load_llm():
    """
    Load the offline LLM model using CTransformers.
    """
    # Model configuration
    llm = CTransformers(
        model=MODEL_CONFIG['model_name'],
        model_type=MODEL_CONFIG['model_type'],
        max_new_tokens=MODEL_CONFIG['max_new_tokens'],
        temperature=MODEL_CONFIG['temperature'],
        top_p=MODEL_CONFIG['top_p'],
        callbacks=[StreamingStdOutCallbackHandler()],
        config={
            'context_length': 2048,
            'gpu_layers': 50  # Adjust based on your GPU memory
        }
    )
    return llm

def load_embeddings():
    """
    Load the embedding model for text vectorization.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    return embeddings

def download_model():
    """
    Download the model if it doesn't exist locally.
    """
    # The model will be downloaded automatically when first used
    print(f"Model will be downloaded to {MODEL_DIR} when first used.")