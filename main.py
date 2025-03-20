from database import init_db
from rag_system import RAGSystem
import argparse
import sys

def setup_database():
    """Initialize the database and create sample data."""
    print("Initializing database and creating sample data...")
    init_db()
    print("Database setup complete!")

def interactive_mode(rag):
    """Run the RAG system in interactive mode."""
    print("\nWelcome to the AI-Powered Retrieval System!")
    print("Type 'exit' or 'quit' to end the session.")
    print("Type 'help' to see example questions.")

    example_questions = [
        "What are the top 5 best-selling products?",
        "Who are our most valuable customers based on total order amount?",
        "What is the average rating for products in the Electronics category?",
        "How many orders were placed in the last month?",
        "Which customers have left the most reviews?"
    ]

    while True:
        try:
            question = input("\nEnter your question: ").strip()

            if question.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            if question.lower() == 'help':
                print("\nExample questions:")
                for i, q in enumerate(example_questions, 1):
                    print(f"{i}. {q}")
                continue

            if not question:
                continue

            print("\nProcessing your question...")
            result = rag.process_question(question)

            if "error" in result:
                print(f"\nError: {result['error']}")
                continue

            print("\nSQL Query:")
            print(result["sql_query"])
            print("\nAnswer:")
            print(result["answer"])

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Retrieval System")
    parser.add_argument("--setup", action="store_true", help="Initialize database and create sample data")
    parser.add_argument("--question", type=str, help="Single question to answer (optional)")

    args = parser.parse_args()

    if args.setup:
        setup_database()
        if not args.question:
            sys.exit(0)

    rag = RAGSystem()

    if args.question:
        result = rag.process_question(args.question)
        if "error" in result:
            print(f"\nError: {result['error']}")
        else:
            print("\nSQL Query:")
            print(result["sql_query"])
            print("\nAnswer:")
            print(result["answer"])
    else:
        interactive_mode(rag)

if __name__ == "__main__":
    main()