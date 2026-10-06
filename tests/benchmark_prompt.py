import time
import os
from agent.prompt_builder import load_prompt, _load_prompt_cached


def run_benchmark(iterations: int = 5000):
    gem_name = "gem1"
    filepath = os.path.join("prompts", f"{gem_name}.md")

    if not os.path.exists(filepath):
        print(f"Prompt file {filepath} not found.")
        return

    mtime = os.path.getmtime(filepath)

    # Measure uncached direct file reading
    start_time = time.perf_counter()
    for _ in range(iterations):
        with open(filepath, "r", encoding="utf-8") as f:
            _ = f.read()
    uncached_total = time.perf_counter() - start_time

    # Warmup cache
    _load_prompt_cached.cache_clear()
    _ = load_prompt(gem_name)

    # Measure cached prompt reading
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = load_prompt(gem_name)
    cached_total = time.perf_counter() - start_time

    speedup = uncached_total / cached_total if cached_total > 0 else 0.0

    print(f"--- Prompt Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached total time: {uncached_total:.4f}s ({uncached_total / iterations * 1e6:.2f} µs/op)")
    print(f"Cached total time:   {cached_total:.4f}s ({cached_total / iterations * 1e6:.2f} µs/op)")
    print(f"Speedup achieved:    {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
