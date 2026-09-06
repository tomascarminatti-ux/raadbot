import os
import time
from agent.prompt_builder import load_prompt, _load_prompt_cached

def benchmark():
    N = 10000

    # Uncached benchmark
    start = time.perf_counter()
    for _ in range(N):
        filepath = os.path.join("prompts", "gem1.md")
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()
    end = time.perf_counter()
    t_uncached = end - start

    # Cached benchmark
    _load_prompt_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(N):
        load_prompt("gem1")
    end = time.perf_counter()
    t_cached = end - start

    print(f"Uncached {N} reads: {t_uncached:.5f}s ({(t_uncached/N)*1000:.4f} ms/call)")
    print(f"Cached {N} reads: {t_cached:.5f}s ({(t_cached/N)*1000:.4f} ms/call)")
    print(f"Speedup: {t_uncached / t_cached:.2f}x")

if __name__ == "__main__":
    benchmark()
