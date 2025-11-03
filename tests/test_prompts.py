import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from app.services.prompt_manager import PromptManager


def test_prompt_templates():
    print("🎨 Testing Prompt Management System\n")
    print("=" * 80)

    print("\n📋 Test 1: Load system prompt")
    print("-" * 80)
    system_prompt = PromptManager.get_prompt("qa_system")
    print(f"System Prompt:\n{system_prompt}")

    print("\n" + "=" * 80)
    print("\n📋 Test 2: Load user prompt with variables")
    print("-" * 80)
    user_prompt = PromptManager.get_prompt(
        "qa_user",
        context="Innovate Inc. holds 12% market share.",
        question="What is Innovate Inc's market share?",
    )
    print(f"User Prompt:\n{user_prompt}")

    print("\n" + "=" * 80)
    print("\n✅ Prompt management test complete!")
    print("\n💡 Benefits of this approach:")
    print("  • Prompts are separated from code (easier to maintain)")
    print("  • Metadata tracking (description, author)")
    print("  • Variable substitution with Jinja2")
    print("  • Reusable across workflows")
    print("  • Version control friendly")


if __name__ == "__main__":
    test_prompt_templates()
