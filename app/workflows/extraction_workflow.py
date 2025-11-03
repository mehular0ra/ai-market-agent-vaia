import os
import json
from openai import OpenAI
from app.database.repository import DocumentRepository
from app.services.prompt_manager import PromptManager


class ExtractionWorkflow:
    def __init__(self):
        self.repo = DocumentRepository()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def run(self) -> dict:
        chunks = self.repo.get_all_chunks()

        if not chunks:
            return {
                "extracted_data": None,
                "error": "No document content available to extract from.",
            }

        context = "\n\n".join([chunk["content"] for chunk in chunks])

        system_prompt = PromptManager.get_prompt("extraction_system")
        user_prompt = PromptManager.get_prompt("extraction_user", context=context)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=1000,
            response_format={"type": "json_object"},
        )

        extracted_text = response.choices[0].message.content

        try:
            extracted_data = json.loads(extracted_text)
        except json.JSONDecodeError as e:
            return {
                "extracted_data": None,
                "error": f"Failed to parse JSON: {str(e)}",
                "raw_response": extracted_text,
            }

        return {
            "extracted_data": extracted_data,
            "chunks_used": len(chunks),
            "model": self.model,
        }
