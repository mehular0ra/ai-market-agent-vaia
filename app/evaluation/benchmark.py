import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import time
import json
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI

from app.services.chunking import ChunkingService
from app.services.embedding import EmbeddingService
from app.database.repository import DocumentRepository

load_dotenv()


class EmbeddingBenchmark:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.repo = DocumentRepository()
        self.embedding_service = EmbeddingService()
        self.test_queries = [
            "What is Innovate Inc's market share?",
            "Who are the main competitors?",
            "What are the key strengths of the product?",
            "What threats does the company face?",
            "What is the projected market growth?",
        ]

    def benchmark_embedding_model(
        self, model_name: str, queries: List[str]
    ) -> Dict[str, Any]:
        print(f"\n📊 Benchmarking embedding model: {model_name}")
        print("-" * 60)

        total_time = 0
        total_tokens = 0
        embeddings = []

        embedding_service = EmbeddingService(model=model_name)

        for query in queries:
            start_time = time.time()
            embedding = embedding_service.generate_embedding(query)
            end_time = time.time()

            total_time += end_time - start_time
            embeddings.append(embedding)

        avg_time = total_time / len(queries)
        dimensions = len(embeddings[0]) if embeddings else 0

        result = {
            "model": model_name,
            "queries_tested": len(queries),
            "total_time_seconds": round(total_time, 3),
            "avg_time_per_query_seconds": round(avg_time, 3),
            "embedding_dimensions": dimensions,
        }

        print(f"  Queries tested: {result['queries_tested']}")
        print(f"  Total time: {result['total_time_seconds']}s")
        print(f"  Avg time per query: {result['avg_time_per_query_seconds']}s")
        print(f"  Embedding dimensions: {result['embedding_dimensions']}")

        return result

    def benchmark_chunking_strategy(
        self, chunk_size: int, chunk_overlap: int, document_path: str
    ) -> Dict[str, Any]:
        print(f"\n📊 Benchmarking chunking: size={chunk_size}, overlap={chunk_overlap}")
        print("-" * 60)

        with open(document_path, "r") as f:
            text = f.read()

        chunking_service = ChunkingService(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

        start_time = time.time()
        chunks = chunking_service.chunk_text(text)
        end_time = time.time()

        total_chars = sum(len(chunk) for chunk in chunks)
        avg_chunk_size = total_chars / len(chunks) if chunks else 0

        result = {
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "num_chunks": len(chunks),
            "total_characters": total_chars,
            "avg_chunk_characters": round(avg_chunk_size, 2),
            "processing_time_seconds": round(end_time - start_time, 3),
        }

        print(f"  Number of chunks: {result['num_chunks']}")
        print(f"  Total characters: {result['total_characters']}")
        print(f"  Avg chunk size: {result['avg_chunk_characters']} chars")
        print(f"  Processing time: {result['processing_time_seconds']}s")

        return result

    def benchmark_retrieval_topk(
        self, query: str, k_values: List[int]
    ) -> Dict[str, Any]:
        print(f"\n📊 Benchmarking retrieval with different top-k values")
        print("-" * 60)
        print(f"Query: {query}")

        query_embedding = self.embedding_service.generate_embedding(query)
        results = {}

        for k in k_values:
            start_time = time.time()
            chunks = self.repo.search_similar_chunks(query_embedding, limit=k)
            end_time = time.time()

            avg_similarity = (
                sum(chunk["similarity"] for chunk in chunks) / len(chunks)
                if chunks
                else 0
            )

            results[f"top_{k}"] = {
                "k": k,
                "chunks_retrieved": len(chunks),
                "avg_similarity": round(avg_similarity, 4),
                "retrieval_time_seconds": round(end_time - start_time, 3),
            }

            print(f"\n  Top-{k}:")
            print(f"    Chunks retrieved: {len(chunks)}")
            print(f"    Avg similarity: {round(avg_similarity, 4)}")
            print(f"    Retrieval time: {round(end_time - start_time, 3)}s")

        return results


def run_full_benchmark():
    print("=" * 80)
    print("🚀 AI MARKET ANALYST - COMPREHENSIVE BENCHMARK")
    print("=" * 80)

    benchmark = EmbeddingBenchmark()
    results = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "benchmarks": {}}

    print("\n" + "=" * 80)
    print("1️⃣  EMBEDDING MODEL COMPARISON")
    print("=" * 80)

    embedding_models = ["text-embedding-3-small", "text-embedding-3-large"]
    embedding_results = []

    for model in embedding_models:
        try:
            result = benchmark.benchmark_embedding_model(model, benchmark.test_queries)
            embedding_results.append(result)
        except Exception as e:
            print(f"  ❌ Error with {model}: {str(e)}")

    results["benchmarks"]["embedding_models"] = embedding_results

    print("\n" + "=" * 80)
    print("2️⃣  CHUNKING STRATEGY COMPARISON")
    print("=" * 80)

    chunking_strategies = [
        {"chunk_size": 250, "chunk_overlap": 50},
        {"chunk_size": 500, "chunk_overlap": 100},
        {"chunk_size": 150, "chunk_overlap": 30},
    ]

    chunking_results = []
    document_path = "data/market_research_report.txt"

    for strategy in chunking_strategies:
        try:
            result = benchmark.benchmark_chunking_strategy(
                strategy["chunk_size"], strategy["chunk_overlap"], document_path
            )
            chunking_results.append(result)
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")

    results["benchmarks"]["chunking_strategies"] = chunking_results

    print("\n" + "=" * 80)
    print("3️⃣  RETRIEVAL TOP-K COMPARISON")
    print("=" * 80)

    k_values = [1, 3, 5, 10]
    test_query = "What is Innovate Inc's market share?"

    try:
        topk_results = benchmark.benchmark_retrieval_topk(test_query, k_values)
        results["benchmarks"]["topk_retrieval"] = topk_results
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

    output_file = "evaluation_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("✅ BENCHMARK COMPLETE")
    print("=" * 80)
    print(f"\n📄 Results saved to: {output_file}")
    print("\n💡 Next steps:")
    print("  1. Review evaluation_results.json")
    print("  2. Check EVALUATION.md for analysis")
    print("  3. Compare metrics across different configurations")

    return results


if __name__ == "__main__":
    run_full_benchmark()
