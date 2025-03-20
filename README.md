# AI-Powered Retrieval System with PostgreSQL and Offline LLM

This project implements a Retrieval-Augmented Generation (RAG) system using PostgreSQL for data storage and an offline LLM for natural language processing. The system can convert natural language questions into SQL queries and provide human-readable answers based on the database content.

## Features

- PostgreSQL database with optimized schema and indexes
- Offline LLM integration using DeepSeek Coder (quantized model)
- Natural language to SQL query conversion
- Interactive CLI interface
- Sample data generation for testing
- Efficient retrieval using RAG techniques

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- At least 8GB RAM
- CUDA-compatible GPU (optional, but recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL:
   - Create a new database named `rag_test_db`
   - Update the database configuration in `config.py` if needed

## Usage

1. Initialize the database and create sample data:
```bash
python main.py --setup
```

2. Run the system in interactive mode:
```bash
python main.py
```

3. Ask a single question:
```bash
python main.py --question "What are the top 5 best-selling products?"
```

## Example Questions

1. What are the top 5 best-selling products?
2. Who are our most valuable customers based on total order amount?
3. What is the average rating for products in the Electronics category?
4. How many orders were placed in the last month?
5. Which customers have left the most reviews?

## Project Structure

- `config.py`: Configuration settings for database and LLM
- `database.py`: Database setup and sample data generation
- `llm_setup.py`: LLM initialization and configuration
- `rag_system.py`: Core RAG implementation
- `main.py`: CLI interface and main application logic

## Performance Optimization

- Database indexes on frequently queried fields
- Quantized LLM model for reduced memory usage
- Efficient SQL query generation
- Optimized schema design

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 