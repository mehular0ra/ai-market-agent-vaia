import os
from openai import OpenAI
from services.retrieval import RetrievalService


class QAWorkflow:
    def __init__(self):
        self.retrieval = RetrievalService()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")

    def run(self, question: str, top_k: int = 3) -> dict:
        context = self.retrieval.get_context_for_query(question, top_k=top_k)

        if not context or context == "No relevant context found.":
            return {
                "question": question,
                "answer": "I don't have enough information to answer this question.",
                "context_used": False,
            }

        system_prompt = """You are a helpful AI assistant analyzing market research data.
Answer questions based ONLY on the provided context.
If the context doesn't contain the answer, say so clearly.
Be concise and specific."""

        user_prompt = f"""Context:
{context}

Question: {question}

Answer:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        answer = response.choices[0].message.content

        return {
            "question": question,
            "answer": answer,
            "context": context,
            "context_used": True,
            "model": self.model,
        }
