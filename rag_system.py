from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document
from sqlalchemy import text
from database import engine
from llm_setup import load_llm, load_embeddings
import json

class RAGSystem:
    def __init__(self):
        self.llm = load_llm()
        self.embeddings = load_embeddings()
        
        # Define the SQL generation prompt
        self.sql_prompt = PromptTemplate(
            input_variables=["question", "schema"],
            template="""Given the following PostgreSQL database schema:
{schema}

Generate a SQL query to answer the following question:
{question}

The query should be efficient and use appropriate JOINs and WHERE clauses.
Return only the SQL query without any explanation.
"""
        )
        
        # Define the answer generation prompt
        self.answer_prompt = PromptTemplate(
            input_variables=["question", "sql_results"],
            template="""Based on the following database query results:
{sql_results}

Answer the following question in a clear and concise way:
{question}

Provide the answer in natural language, explaining the key insights from the data.
"""
        )
        
        # Create chains
        self.sql_chain = LLMChain(llm=self.llm, prompt=self.sql_prompt)
        self.answer_chain = LLMChain(llm=self.llm, prompt=self.answer_prompt)
    
    def get_schema_info(self):
        """Get the database schema information."""
        schema_info = """
        Tables:
        1. customers
           - customer_id (PK)
           - name
           - email
           - phone
           - address
           - registration_date
        
        2. products
           - product_id (PK)
           - name
           - description
           - price
           - category
           - stock_quantity
        
        3. orders
           - order_id (PK)
           - customer_id (FK)
           - order_date
           - total_amount
           - status
        
        4. order_items
           - item_id (PK)
           - order_id (FK)
           - product_id (FK)
           - quantity
           - unit_price
        
        5. reviews
           - review_id (PK)
           - product_id (FK)
           - customer_id (FK)
           - rating
           - comment
           - review_date
        """
        return schema_info
    
    def execute_sql(self, query):
        """Execute the SQL query and return results."""
        try:
            with engine.connect() as connection:
                result = connection.execute(text(query))
                columns = result.keys()
                rows = [dict(zip(columns, row)) for row in result.fetchall()]
                return rows
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def format_results(self, results):
        """Format the SQL results for the LLM."""
        if isinstance(results, str):  # Error message
            return results
        
        if not results:
            return "No results found."
        
        return json.dumps(results, indent=2, default=str)
    
    def process_question(self, question):
        """Process a natural language question and return an answer."""
        try:
            # Generate SQL query
            sql_query = self.sql_chain.run({
                "question": question,
                "schema": self.get_schema_info()
            }).strip()
            
            # Execute the query
            results = self.execute_sql(sql_query)
            formatted_results = self.format_results(results)
            
            # Generate natural language answer
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