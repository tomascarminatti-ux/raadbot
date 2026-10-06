"""
benchmark_prompt.py – Benchmark script for prompt template loading and variable extraction.
"""

import time
from agent.prompt_builder import build_prompt, _load_prompt_cached


def run_benchmark():
    vars_gem1 = {
        "search_id": "BENCHMARK-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced software architect with 10+ years of domain experience.",
        "interview_notes": "Strong communication, excellent system design skills.",
        "gem5_summary": "High-impact tech lead position for scaling distributed systems.",
    }

    iterations = 2000

    # Benchmark without cache (clearing cache on each call)
    _load_prompt_cached.cache_clear()
    t0 = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        build_prompt("gem1", vars_gem1)
    t1 = time.perf_counter()
    uncached_time = t1 - t0

    # Warmup cache
    _load_prompt_cached.cache_clear()
    build_prompt("gem1", vars_gem1)

    # Benchmark with cache
    t2 = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", vars_gem1)
    t3 = time.perf_counter()
    cached_time = t3 - t2

    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print("=== PROMPT BUILDER BENCHMARK ===")
    print(f"Iterations: {iterations}")
    print(f"Uncached total time: {uncached_time * 1000:.2f} ms ({uncached_time / iterations * 1000:.4f} ms/op)")
    print(f"Cached total time:   {cached_time * 1000:.2f} ms ({cached_time / iterations * 1000:.4f} ms/op)")
    print(f"Speedup:             {speedup:.2f}x faster")


if __name__ == "__main__":
    run_benchmark()
