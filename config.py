from pathlib import Path

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'rag_test_db',
    'user': 'abdulrazaque',  # Using system username
    'password': ''  # No password needed for local development
}

# Model Configuration
MODEL_CONFIG = {
    'model_name': 'TheBloke/deepseek-coder-1.3b-base-GGUF',  # Using GGUF format model
    'model_type': 'deepseek',
    'max_new_tokens': 256,
    'temperature': 0.7,
    'top_p': 0.95,
    'context_length': 1024,
    'gpu_layers': 0
}

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)