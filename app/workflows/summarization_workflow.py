import os
from openai import OpenAI
from app.database.repository import DocumentRepository
from app.services.prompt_manager import PromptManager


class SummarizationWorkflow:
    def __init__(self):
        self.repo = DocumentRepository()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def run(self) -> dict:
        chunks = self.repo.get_all_chunks()

        if not chunks:
            return {
                "summary": "No document content available to summarize.",
                "chunks_used": 0,
            }

        context = "\n\n".join([chunk["content"] for chunk in chunks])

        system_prompt = PromptManager.get_prompt("summarization_system")
        user_prompt = PromptManager.get_prompt("summarization_user", context=context)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=800,
        )

        summary = response.choices[0].message.content

        return {
            "summary": summary,
            "chunks_used": len(chunks),
            "model": self.model,
        }
