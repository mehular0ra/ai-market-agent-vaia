import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from dotenv import load_dotenv
from workflows.extraction_workflow import ExtractionWorkflow

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


def test_extraction_workflow():
    print("🔍 Testing Data Extraction Workflow\n")
    print("=" * 80)

    extraction = ExtractionWorkflow()

    print("\n🔄 Extracting structured data...")
    print("-" * 80)

    result = extraction.run()

    if result.get("error"):
        print(f"\n❌ Error: {result['error']}")
        if result.get("raw_response"):
            print(f"\nRaw response:\n{result['raw_response']}")
        return

    print(f"\n📊 Extracted Data:")
    print("-" * 80)
    print(json.dumps(result["extracted_data"], indent=2))

    print(f"\n📊 Metadata:")
    print(f"  Model: {result['model']}")
    print(f"  Chunks used: {result['chunks_used']}")

    print("\n" + "=" * 80)
    print("\n✅ Data extraction workflow test complete!")


if __name__ == "__main__":
    test_extraction_workflow()
