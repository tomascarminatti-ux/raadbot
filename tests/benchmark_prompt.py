"""
benchmark_prompt.py – Benchmark script for comparing prompt loading and building speed before and after caching.
"""

import os
import time
from agent.prompt_builder import load_prompt, build_prompt, _load_prompt_cached

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

def uncached_load_prompt(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def run_benchmark():
    iterations = 5000
    vars_dict = {
        "candidate_name": "Juan Perez",
        "role": "Senior Software Engineer",
        "input": {"experience": "10 years", "skills": ["Python", "FastAPI"]}
    }

    # Clear cache before benchmarking
    _load_prompt_cached.cache_clear()

    # Benchmark uncached loading
    start = time.perf_counter()
    for _ in range(iterations):
        uncached_load_prompt("gem1")
        uncached_load_prompt("00_prompt_maestro")
    uncached_time = time.perf_counter() - start

    # Benchmark cached loading
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem1")
        load_prompt("00_prompt_maestro")
    cached_time = time.perf_counter() - start

    # Benchmark build_prompt with cached loading
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", vars_dict)
    build_time = time.perf_counter() - start

    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print("=== PROMPT BUILDER BENCHMARK RESULTS ===")
    print(f"Iterations: {iterations}")
    print(f"Uncached File Loading: {uncached_time:.4f} seconds")
    print(f"Cached File Loading:   {cached_time:.4f} seconds")
    print(f"Build Prompt Total:    {build_time:.4f} seconds")
    print(f"Loading Speedup:       {speedup:.2f}x faster")

if __name__ == "__main__":
    run_benchmark()
