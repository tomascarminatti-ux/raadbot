import time
import functools
import os
from agent.prompt_builder import build_prompt, _load_prompt_cached, load_prompt


def benchmark():
    _load_prompt_cached.cache_clear()

    iterations = 5000

    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", {"candidate_name": "Juan Perez", "position": "Senior Engineer"})
    elapsed = time.perf_counter() - start

    info = _load_prompt_cached.cache_info()

    print(f"--- Benchmark Prompt Builder ---")
    print(f"Total time for {iterations} calls: {elapsed:.4f}s")
    print(f"Average time per call: {elapsed/iterations*1000:.4f}ms")
    print(f"Cache Hits: {info.hits}, Cache Misses: {info.misses}")


if __name__ == "__main__":
    benchmark()
