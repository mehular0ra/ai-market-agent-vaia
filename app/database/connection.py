import psycopg2
from psycopg2.extras import RealDictCursor
from database.config import DatabaseConfig


def get_connection():
    return psycopg2.connect(
        DatabaseConfig.get_connection_string(), cursor_factory=RealDictCursor
    )


def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            embedding vector(1536),
            chunk_index INTEGER NOT NULL,
            metadata JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS embedding_idx 
        ON document_chunks 
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
    """)

    conn.commit()
    cur.close()
    conn.close()

    print("Database initialized successfully!")
