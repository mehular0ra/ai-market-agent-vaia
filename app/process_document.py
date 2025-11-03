import os
from dotenv import load_dotenv
from services.chunking import ChunkingService
from services.embedding import EmbeddingService
from database.repository import DocumentRepository

load_dotenv()


def process_market_report():
    report_path = "../data/market_research_report.txt"

    with open(report_path, "r") as f:
        document_text = f.read()

    print(f"Loaded document: {len(document_text)} characters")

    chunk_size = int(os.getenv("CHUNK_SIZE", 250))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 50))

    chunker = ChunkingService(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = chunker.chunk_text(document_text)

    print(f"Created {len(chunks)} chunks")

    embedder = EmbeddingService()
    print(f"Generating embeddings using {embedder.model}...")

    embeddings = embedder.generate_embeddings_batch(chunks)

    print(f"Generated {len(embeddings)} embeddings")

    repo = DocumentRepository()
    repo.clear_all_chunks()

    print("Storing chunks in database...")
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        repo.insert_chunk(
            content=chunk,
            embedding=embedding,
            chunk_index=i,
            metadata={"source": "market_research_report.txt"},
        )

    print(f"Successfully processed and stored {len(chunks)} chunks!")

    stored_chunks = repo.get_all_chunks()
    print(f"\nVerification: {len(stored_chunks)} chunks in database")
    print("\nFirst chunk preview:")
    print(f"  Index: {stored_chunks[0]['chunk_index']}")
    print(f"  Content: {stored_chunks[0]['content'][:100]}...")


if __name__ == "__main__":
    process_market_report()
