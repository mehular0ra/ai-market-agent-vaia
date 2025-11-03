#!/bin/bash

echo "🧪 Running All Tests"
echo "===================="
echo ""

echo "1️⃣  Testing Prompt Management..."
uv run python tests/test_prompts.py
echo ""

echo "2️⃣  Testing RAG Retrieval..."
uv run python tests/test_retrieval.py
echo ""

echo "3️⃣  Testing Q&A Workflow..."
uv run python tests/test_qa.py
echo ""

echo "4️⃣  Testing Summarization Workflow..."
uv run python tests/test_summarization.py
echo ""

echo "5️⃣  Testing Data Extraction Workflow..."
uv run python tests/test_extraction.py
echo ""

echo "6️⃣  Testing Query Router..."
uv run python tests/test_router.py
echo ""

echo "7️⃣  Testing API Endpoints..."
uv run python tests/test_api.py
echo ""

echo "✅ All tests complete!"

