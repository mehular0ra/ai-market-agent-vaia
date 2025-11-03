from typing import List, Dict, Any
from psycopg2.extras import Json
from database.connection import get_connection


class DocumentRepository:
    def insert_chunk(
        self,
        content: str,
        embedding: List[float],
        chunk_index: int,
        metadata: Dict = None,
    ):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO document_chunks (content, embedding, chunk_index, metadata)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """,
            (content, embedding, chunk_index, Json(metadata)),
        )

        chunk_id = cur.fetchone()["id"]
        conn.commit()
        cur.close()
        conn.close()

        return chunk_id

    def search_similar_chunks(
        self, query_embedding: List[float], limit: int = 5
    ) -> List[Dict[str, Any]]:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, content, chunk_index, metadata,
                   1 - (embedding <=> %s::vector) as similarity
            FROM document_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """,
            (query_embedding, query_embedding, limit),
        )

        results = cur.fetchall()
        cur.close()
        conn.close()

        return results

    def get_all_chunks(self) -> List[Dict[str, Any]]:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, content, chunk_index FROM document_chunks ORDER BY chunk_index;"
        )
        results = cur.fetchall()

        cur.close()
        conn.close()

        return results

    def clear_all_chunks(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM document_chunks;")
        conn.commit()

        cur.close()
        conn.close()
