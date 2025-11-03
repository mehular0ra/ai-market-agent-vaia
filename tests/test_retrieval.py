import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from app.services.retrieval import RetrievalService

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def test_retrieval():
    retrieval = RetrievalService()

    test_queries = [
        "What is Innovate Inc's market share?",
        "Who are the main competitors?",
        "What are the growth opportunities?",
        "What is the market size?",
    ]

    print("Testing RAG Retrieval Service\n")
    print("=" * 80)

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 80)

        chunks = retrieval.retrieve_relevant_chunks(query, top_k=2)

        for i, chunk in enumerate(chunks, 1):
            similarity = chunk.get("similarity", 0)
            content_preview = chunk["content"][:150].replace("\n", " ")

            print(f"\n  Chunk {i} (Similarity: {similarity:.4f})")
            print(f"  Index: {chunk['chunk_index']}")
            print(f"  Content: {content_preview}...")

        print("\n" + "=" * 80)

    print("\nRetrieval test complete!")

    print("\n\nTesting context generation:")
    print("=" * 80)
    query = "What are Innovate Inc's strengths and weaknesses?"
    print(f"Query: {query}\n")

    context = retrieval.get_context_for_query(query, top_k=2)
    print("Generated Context:")
    print(context)


if __name__ == "__main__":
    test_retrieval()
