import time
import os
import sys
import json
import asyncio
import functools
import re

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import build_prompt
from utils.gem_core import GEMClient

def benchmark_prompt_builder():
    print("Benchmarking prompt_builder...")
    variables = {
        "search_id": "BENCHMARK-001",
        "candidate_id": "CAND-001",
        "context": {"some": "data", "more": "data"}
    }

    # Warmup
    for _ in range(10):
        build_prompt("gem6", variables)

    start = time.time()
    iterations = 500
    for _ in range(iterations):
        build_prompt("gem6", variables)
    end = time.time()

    avg_time = (end - start) / iterations
    print(f"Average build_prompt time: {avg_time*1000:.4f} ms")
    return avg_time

async def benchmark_gem_client():
    print("Benchmarking GEMClient...")
    client = GEMClient(db_url="http://localhost:12345") # Non-existent port to measure overhead
    data = {"entity_id": "test", "state": "test"}

    start = time.time()
    iterations = 50
    for _ in range(iterations):
        await client.upsert_entity(data)
    end = time.time()

    avg_time = (end - start) / iterations
    print(f"Average GEMClient overhead time: {avg_time*1000:.4f} ms")
    return avg_time

async def main():
    prompt_time = benchmark_prompt_builder()
    client_time = await benchmark_gem_client()

    results = {
        "prompt_builder_ms": prompt_time * 1000,
        "gem_client_ms": client_time * 1000
    }
    with open("benchmark_results_pre.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    asyncio.run(main())
