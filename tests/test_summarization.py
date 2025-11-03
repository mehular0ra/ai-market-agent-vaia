import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from dotenv import load_dotenv
from workflows.summarization_workflow import SummarizationWorkflow

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def test_summarization_workflow():
    print("📊 Testing Summarization Workflow\n")
    print("=" * 80)

    summarization = SummarizationWorkflow()

    print("\n🔄 Generating executive summary...")
    print("-" * 80)

    result = summarization.run()

    print(f"\n📝 Executive Summary:")
    print("-" * 80)
    print(result["summary"])

    print(f"\n📊 Metadata:")
    print(f"  Model: {result['model']}")
    print(f"  Chunks used: {result['chunks_used']}")

    print("\n" + "=" * 80)
    print("\n✅ Summarization workflow test complete!")


if __name__ == "__main__":
    test_summarization_workflow()
