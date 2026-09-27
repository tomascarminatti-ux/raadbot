import time
import os
import functools
from agent.prompt_builder import load_prompt, build_prompt, _load_prompt_cached

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

def uncached_load_prompt(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def run_benchmark():
    iterations = 2000
    vars_data = {"input": {"role": "Senior Staff Engineer", "location": "Madrid"}}

    # Benchmark uncached prompt loading
    t0 = time.perf_counter()
    for _ in range(iterations):
        uncached_load_prompt("gem5")
    uncached_time = time.perf_counter() - t0

    # Benchmark cached prompt loading
    _load_prompt_cached.cache_clear()
    t0 = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem5")
    cached_time = time.perf_counter() - t0

    speedup = uncached_time / cached_time if cached_time > 0 else 0.0

    print("=" * 60)
    print(f"Benchmark: Prompt Template Loading ({iterations} iterations)")
    print(f"  Uncached time: {uncached_time:.4f}s ({uncached_time/iterations*1000:.4f} ms/op)")
    print(f"  Cached time:   {cached_time:.4f}s ({cached_time/iterations*1000:.4f} ms/op)")
    print(f"  Speedup:       {speedup:.2f}x faster")
    print("=" * 60)

if __name__ == "__main__":
    run_benchmark()
