import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from dotenv import load_dotenv
from app.workflows.qa_workflow import QAWorkflow

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def test_qa_workflow():
    qa = QAWorkflow()

    test_questions = [
        "What is Innovate Inc's market share?",
        "Who are the main competitors and what are their market shares?",
        "What are Innovate Inc's strengths?",
        "What is the projected market size by 2030?",
        "What is the CAGR for the AI workflow automation market?",
        "What are the key threats to Innovate Inc?",
    ]

    print("🤖 Testing Q&A Workflow\n")
    print("=" * 80)

    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 80)

        result = qa.run(question, top_k=2)

        print(f"\n💡 Answer:")
        print(result["answer"])

        print(f"\n📊 Metadata:")
        print(f"  Model: {result['model']}")
        print(f"  Context used: {result['context_used']}")

        print("\n" + "=" * 80)

    print("\n✅ Q&A workflow test complete!")


if __name__ == "__main__":
    test_qa_workflow()
