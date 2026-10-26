"""
benchmark_prompt.py – Benchmark para medir el rendimiento de build_prompt.
"""

import time
import os
from agent.prompt_builder import build_prompt, _load_prompt_cached


def run_benchmark(iterations: int = 2000):
    vars_gem1 = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Software Engineer with 10 years experience",
        "interview_notes": "Great candidate",
        "gem5_summary": "Summary of gem5",
    }

    # Clear cache for cold start measurement
    _load_prompt_cached.cache_clear()

    # Warmup
    _ = build_prompt("gem1", vars_gem1)

    start = time.perf_counter()
    for _ in range(iterations):
        _ = build_prompt("gem1", vars_gem1)
    elapsed = time.perf_counter() - start

    cache_info = _load_prompt_cached.cache_info()

    print(f"--- Benchmark Prompt Builder ---")
    print(f"Ejecuciones: {iterations}")
    print(f"Tiempo total: {elapsed * 1000:.2f} ms")
    print(f"Tiempo promedio por op: {elapsed / iterations * 1000:.4f} ms")
    print(f"Cache Hits: {cache_info.hits}, Misses: {cache_info.misses}")

    return elapsed


if __name__ == "__main__":
    run_benchmark()
