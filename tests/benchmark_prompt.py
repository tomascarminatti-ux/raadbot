import os
import time
from agent.prompt_builder import load_prompt, _load_prompt_cached


def benchmark():
    n_iterations = 10000

    # Uncached benchmark
    start = time.perf_counter()
    for _ in range(n_iterations):
        filepath = os.path.join("prompts", "gem1.md")
        with open(filepath, "r", encoding="utf-8") as f:
            _ = f.read()
    end = time.perf_counter()
    t_uncached = end - start

    # Cached benchmark
    _load_prompt_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(n_iterations):
        load_prompt("gem1")
    end = time.perf_counter()
    t_cached = end - start

    uncached_ms = (t_uncached / n_iterations) * 1000
    cached_ms = (t_cached / n_iterations) * 1000
    print(f"Uncached {n_iterations} reads: "
          f"{t_uncached:.5f}s ({uncached_ms:.4f} ms/call)")
    print(f"Cached {n_iterations} reads: "
          f"{t_cached:.5f}s ({cached_ms:.4f} ms/call)")
    print(f"Speedup: {t_uncached / t_cached:.2f}x")


if __name__ == "__main__":
    benchmark()
