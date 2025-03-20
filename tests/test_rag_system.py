import unittest
from rag_system import RAGSystem
from database import init_db, engine
from sqlalchemy.orm import sessionmaker

class TestRAGSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database and RAG system."""
        init_db()  # Initialize database with sample data
        cls.rag = RAGSystem()
    
    def test_simple_query(self):
        """Test a simple query about products."""
        question = "What are the top 5 best-selling products?"
        result = self.rag.process_question(question)
        
        self.assertIn("sql_query", result)
        self.assertIn("answer", result)
        self.assertNotIn("error", result)
    
    def test_complex_query(self):
        """Test a complex query involving multiple tables."""
        question = "What is the average rating for products in the Electronics category?"
        result = self.rag.process_question(question)
        
        self.assertIn("sql_query", result)
        self.assertIn("answer", result)
        self.assertNotIn("error", result)
    
    def test_invalid_query(self):
        """Test handling of invalid questions."""
        question = "What is the meaning of life?"
        result = self.rag.process_question(question)
        
        self.assertIn("sql_query", result)  # Should still generate a query
        self.assertIn("answer", result)  # Should handle gracefully
    
    def test_schema_info(self):
        """Test schema information retrieval."""
        schema = self.rag.get_schema_info()
        
        self.assertIn("customers", schema)
        self.assertIn("products", schema)
        self.assertIn("orders", schema)
        self.assertIn("reviews", schema)

if __name__ == '__main__':
    unittest.main() 