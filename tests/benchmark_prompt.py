import time
import os
from agent.prompt_builder import build_prompt, _load_prompt_cached


def run_benchmark(iterations: int = 1000):
    """Benchmark prompt loading performance with and without LRU cache."""
    print(f"Running prompt builder benchmark with {iterations} iterations...")

    # Clear cache for uncached measurement
    _load_prompt_cached.cache_clear()

    # Measure uncached / cache-cleared loading
    start_time = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        build_prompt("gem1", {"candidate_name": "Test Candidate", "jd_text": "Senior Engineer"})
    uncached_time = time.perf_counter() - start_time

    # Warm up cache once
    build_prompt("gem1", {"candidate_name": "Test Candidate", "jd_text": "Senior Engineer"})

    # Measure cached loading
    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", {"candidate_name": "Test Candidate", "jd_text": "Senior Engineer"})
    cached_time = time.perf_counter() - start_time

    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print(f"Uncached execution time: {uncached_time * 1000:.2f} ms ({uncached_time / iterations * 1e6:.2f} µs/call)")
    print(f"Cached execution time:   {cached_time * 1000:.2f} ms ({cached_time / iterations * 1e6:.2f} µs/call)")
    print(f"Speedup achieved:        {speedup:.2f}x")

    return speedup


if __name__ == "__main__":
    run_benchmark()
