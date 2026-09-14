import os
import time
from agent.prompt_builder import load_prompt, build_prompt, clear_prompt_caches, PROMPTS_DIR


def benchmark_prompt_loading(iterations: int = 10000):
    clear_prompt_caches()

    # Benchmark uncached reading
    filepath = os.path.join(PROMPTS_DIR, "gem6.md")
    t0 = time.perf_counter()
    for _ in range(iterations):
        with open(filepath, "r", encoding="utf-8") as f:
            _ = f.read()
    t1 = time.perf_counter()
    uncached_time = t1 - t0

    # Benchmark cached load_prompt
    t0 = time.perf_counter()
    for _ in range(iterations):
        _ = load_prompt("gem6")
    t1 = time.perf_counter()
    cached_time = t1 - t0

    speedup = uncached_time / cached_time if cached_time > 0 else float("inf")
    print(f"\n--- Benchmark Prompt Loading ({iterations} iterations) ---")
    print(f"Uncached load time: {uncached_time:.4f}s ({uncached_time/iterations*1e6:.2f} µs/op)")
    print(f"Cached load time:   {cached_time:.4f}s ({cached_time/iterations*1e6:.2f} µs/op)")
    print(f"Speedup factor:     {speedup:.2f}x")

    return speedup


if __name__ == "__main__":
    benchmark_prompt_loading()
