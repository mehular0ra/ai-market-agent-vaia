from typing import List, Dict, Any
from services.embedding import EmbeddingService
from database.repository import DocumentRepository


class RetrievalService:
    def __init__(self):
        self.embedder = EmbeddingService()
        self.repo = DocumentRepository()

    def retrieve_relevant_chunks(
        self, query: str, top_k: int = 3
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.generate_embedding(query)
        results = self.repo.search_similar_chunks(
            query_embedding=query_embedding, limit=top_k
        )
        return results

    def get_context_for_query(self, query: str, top_k: int = 3) -> str:
        chunks = self.retrieve_relevant_chunks(query, top_k)

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Chunk {i}]\n{chunk['content']}")

        return "\n\n".join(context_parts)
