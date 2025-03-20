from pathlib import Path

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'rag_test_db',
    'user': 'postgres',
    'password': 'postgres'  # Change this in production
}

# Model Configuration
MODEL_CONFIG = {
    'model_name': 'TheBloke/deepseek-coder-6.7B-base.Q4_K_M',  # Quantized model
    'model_type': 'deepseek',
    'max_new_tokens': 512,
    'temperature': 0.7,
    'top_p': 0.95
}

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
MODEL_DIR = BASE_DIR / 'models'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True) 