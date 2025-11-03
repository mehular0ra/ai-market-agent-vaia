import os
from openai import OpenAI
from .prompt_manager import PromptManager


class QueryRouter:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def route(self, query: str) -> str:
        prompt = PromptManager.get_prompt("router", query=query)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=10,
        )

        route = response.choices[0].message.content.strip().lower()

        if route not in ["qa", "summarization", "extraction"]:
            return "qa"

        return route
