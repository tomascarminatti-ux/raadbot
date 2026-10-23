"""
benchmark_prompt.py - Measures performance of prompt loading caching.
"""

import time
from agent.prompt_builder import load_prompt, _load_prompt_cached


def benchmark():
    _load_prompt_cached.cache_clear()

    iterations = 5000

    start = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        load_prompt("gem1")
        load_prompt("00_prompt_maestro")
    uncached_time = time.perf_counter() - start

    _load_prompt_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem1")
        load_prompt("00_prompt_maestro")
    cached_time = time.perf_counter() - start

    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print(f"--- Prompt Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached Time: {uncached_time:.4f} seconds")
    print(f"Cached Time:   {cached_time:.4f} seconds")
    print(f"Speedup:       {speedup:.2f}x faster")


if __name__ == "__main__":
    benchmark()
