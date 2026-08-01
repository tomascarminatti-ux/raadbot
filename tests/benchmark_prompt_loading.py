import time
import os
from agent.prompt_builder import load_prompt, _load_prompt_cached

def benchmark():
    print("=== Prompt Loading Cache Benchmark ===")

    # Warm up / Load once
    gem_name = "gem1"

    # Uncached Load (Simulated by clearing the cache before call)
    iterations = 1000

    _load_prompt_cached.cache_clear()

    start_uncached = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        load_prompt(gem_name)
    end_uncached = time.perf_counter()
    uncached_duration = end_uncached - start_uncached

    # Cached Load
    _load_prompt_cached.cache_clear()
    # Load once to populate cache
    load_prompt(gem_name)

    start_cached = time.perf_counter()
    for _ in range(iterations):
        load_prompt(gem_name)
    end_cached = time.perf_counter()
    cached_duration = end_cached - start_cached

    speedup = uncached_duration / cached_duration if cached_duration > 0 else float('inf')

    print(f"Iterations: {iterations}")
    print(f"Uncached Time (Disk IO): {uncached_duration:.6f} seconds (Avg: {uncached_duration/iterations*1000:.4f} ms/call)")
    print(f"Cached Time (LRU Cache): {cached_duration:.6f} seconds (Avg: {cached_duration/iterations*1000:.4f} ms/call)")
    print(f"Performance Speedup: {speedup:.2f}x faster!")
    print("======================================")

if __name__ == "__main__":
    benchmark()
