import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector
from database.config import DatabaseConfig


def get_connection():
    conn = psycopg2.connect(
        DatabaseConfig.get_connection_string(), cursor_factory=RealDictCursor
    )
    register_vector(conn)
    return conn


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
