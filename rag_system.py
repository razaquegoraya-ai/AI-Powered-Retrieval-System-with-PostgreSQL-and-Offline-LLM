from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document
from sqlalchemy import text
from database import engine
from llm_setup import load_llm, load_embeddings
import json
from functools import lru_cache

class RAGSystem:
    def __init__(self):
        self.llm = load_llm()
        self.embeddings = load_embeddings()
        
        # Define the SQL generation prompt with optimized template
        self.sql_prompt = PromptTemplate(
            input_variables=["question", "schema"],
            template="""Schema:
{schema}

Question: {question}

Generate SQL query only. No explanation."""
        )
        
        # Define the answer generation prompt with optimized template
        self.answer_prompt = PromptTemplate(
            input_variables=["question", "sql_results"],
            template="""Results: {sql_results}

Question: {question}

Answer:"""
        )
        
        # Create chains with optimized settings
        self.sql_chain = LLMChain(
            llm=self.llm,
            prompt=self.sql_prompt,
            verbose=False  # Disable verbose output
        )
        self.answer_chain = LLMChain(
            llm=self.llm,
            prompt=self.answer_prompt,
            verbose=False  # Disable verbose output
        )
    
    @lru_cache(maxsize=1)
    def get_schema_info(self):
        """Get the database schema information with caching."""
        schema_info = """
        Tables:
        1. customers (customer_id, name, email, phone, address, registration_date)
        2. products (product_id, name, description, price, category, stock_quantity)
        3. orders (order_id, customer_id, order_date, total_amount, status)
        4. order_items (item_id, order_id, product_id, quantity, unit_price)
        5. reviews (review_id, product_id, customer_id, rating, comment, review_date)
        """
        return schema_info
    
    def execute_sql(self, query):
        """Execute the SQL query with optimized connection handling."""
        try:
            with engine.connect() as connection:
                result = connection.execute(text(query))
                return [dict(zip(result.keys(), row)) for row in result.fetchall()]
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def format_results(self, results):
        """Format the SQL results efficiently."""
        if isinstance(results, str):
            return results
        if not results:
            return "No results found."
        return json.dumps(results, indent=2, default=str)
    
    def process_question(self, question):
        """Process a question with optimized pipeline."""
        try:
            # Generate SQL query
            sql_query = self.sql_chain.run({
                "question": question,
                "schema": self.get_schema_info()
            }).strip()
            
            # Execute query
            results = self.execute_sql(sql_query)
            formatted_results = self.format_results(results)
            
            # Generate answer
            answer = self.answer_chain.run({
                "question": question,
                "sql_results": formatted_results
            })
            
            return {
                "question": question,
                "sql_query": sql_query,
                "results": results,
                "answer": answer
            }
        
        except Exception as e:
            return {
                "error": f"Error processing question: {str(e)}",
                "question": question
            }

def test_rag_system():
    """Test the RAG system with sample questions."""
    rag = RAGSystem()
    
    test_questions = [
        "What are the top 5 best-selling products?",
        "Who are our most valuable customers based on total order amount?",
        "What is the average rating for products in the Electronics category?",
        "How many orders were placed in the last month?",
        "Which customers have left the most reviews?"
    ]
    
    for question in test_questions:
        print("\nQuestion:", question)
        result = rag.process_question(question)
        print("\nSQL Query:", result.get("sql_query", "N/A"))
        print("\nAnswer:", result.get("answer", "N/A"))
        print("-" * 80)

if __name__ == "__main__":
    test_rag_system() 