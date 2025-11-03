import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from app.api.main import app

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

client = TestClient(app)


def test_api():
    print("🌐 Testing API Endpoints\n")
    print("=" * 80)

    print("\n📍 Test 1: Root endpoint")
    print("-" * 80)
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\n" + "=" * 80)
    print("\n📍 Test 2: Q&A endpoint")
    print("-" * 80)
    response = client.post(
        "/qa", json={"query": "What is the market share?", "top_k": 2}
    )
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Workflow: {result['workflow']}")
    print(f"Answer: {result['result']['answer'][:100]}...")

    print("\n" + "=" * 80)
    print("\n📍 Test 3: Summarization endpoint")
    print("-" * 80)
    response = client.post("/summarize")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Workflow: {result['workflow']}")
    print(f"Summary (first 200 chars): {result['result']['summary'][:200]}...")

    print("\n" + "=" * 80)
    print("\n📍 Test 4: Extraction endpoint")
    print("-" * 80)
    response = client.post("/extract")
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Workflow: {result['workflow']}")
    print(f"Company: {result['result']['extracted_data']['company_name']}")
    print(
        f"Market Share: {result['result']['extracted_data']['market_share_percent']}%"
    )

    print("\n" + "=" * 80)
    print("\n📍 Test 5: Auto-routing endpoint")
    print("-" * 80)

    test_queries = [
        "What are the competitors?",
        "Summarize the key findings",
        "Extract the SWOT analysis",
    ]

    for query in test_queries:
        response = client.post("/query", json={"query": query, "top_k": 2})
        result = response.json()
        print(f"\nQuery: {query}")
        print(f"Routed to: {result['workflow']}")

    print("\n" + "=" * 80)
    print("\n✅ API test complete!")


if __name__ == "__main__":
    test_api()
