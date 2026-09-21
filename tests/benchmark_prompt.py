import time
from agent.prompt_builder import load_prompt, build_prompt, _load_prompt_cached, PROMPTS_DIR
import os


def benchmark_prompt_loading():
    iterations = 2000
    gem_name = "gem1"
    filepath = os.path.join(PROMPTS_DIR, f"{gem_name}.md")

    # 1. Benchmark without cache (forcing disk read each time)
    start_uncached = time.perf_counter()
    for _ in range(iterations):
        with open(filepath, "r", encoding="utf-8") as f:
            _ = f.read()
    uncached_duration = time.perf_counter() - start_uncached

    # 2. Benchmark with LRU cache
    _load_prompt_cached.cache_clear()
    # Warmup
    load_prompt(gem_name)

    start_cached = time.perf_counter()
    for _ in range(iterations):
        _ = load_prompt(gem_name)
    cached_duration = time.perf_counter() - start_cached

    speedup = uncached_duration / cached_duration if cached_duration > 0 else float("inf")

    print(f"\n--- Prompt Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached File I/O Time : {uncached_duration:.5f}s")
    print(f"LRU Cached Time        : {cached_duration:.5f}s")
    print(f"Speedup                : {speedup:.2f}x faster\n")

    assert speedup > 2.0, f"Expected at least 2.0x speedup, got {speedup:.2f}x"


if __name__ == "__main__":
    benchmark_prompt_loading()
