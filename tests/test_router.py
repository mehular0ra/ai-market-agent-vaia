import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from app.services.router import QueryRouter

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def test_router():
    print("🔀 Testing Query Router\n")
    print("=" * 80)

    router = QueryRouter()

    test_queries = [
        ("What is Innovate Inc's market share?", "qa"),
        ("Who are the main competitors?", "qa"),
        ("What are the threats?", "qa"),
        ("Summarize the report", "summarization"),
        ("Give me an overview", "summarization"),
        ("What are the key findings?", "summarization"),
        ("Extract all competitors", "extraction"),
        ("Get the SWOT analysis as JSON", "extraction"),
        ("List all the data points", "extraction"),
    ]

    correct = 0
    total = len(test_queries)

    for query, expected_route in test_queries:
        actual_route = router.route(query)
        is_correct = actual_route == expected_route
        correct += is_correct

        status = "✅" if is_correct else "❌"
        print(f"\n{status} Query: {query}")
        print(f"   Expected: {expected_route}")
        print(f"   Actual: {actual_route}")

    print("\n" + "=" * 80)
    print(f"\n📊 Results: {correct}/{total} correct ({correct / total * 100:.1f}%)")
    print("\n✅ Router test complete!")


if __name__ == "__main__":
    test_router()
