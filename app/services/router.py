import os
from openai import OpenAI


class QueryRouter:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def route(self, query: str) -> str:
        system_prompt = """You are a query router for a market research analysis system.
Classify the user's query into one of these categories:

1. "qa" - For specific questions about the market research data
   Examples: "What is the market share?", "Who are the competitors?", "What are the threats?"

2. "summarization" - For requests to summarize or provide an overview
   Examples: "Summarize the report", "Give me an overview", "What are the key findings?"

3. "extraction" - For requests to extract structured data or specific fields
   Examples: "Extract all competitors", "Get the SWOT analysis as JSON", "List all the data points"

Respond with ONLY one word: "qa", "summarization", or "extraction"."""

        user_prompt = f"Query: {query}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=10,
        )

        route = response.choices[0].message.content.strip().lower()

        if route not in ["qa", "summarization", "extraction"]:
            return "qa"

        return route

