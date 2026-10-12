"""
benchmark_prompt.py - Benchmarks template loading performance with LRU caching vs uncached file I/O.
"""

import time
import os
import functools
import re
from agent.prompt_builder import PROMPTS_DIR, build_prompt, _load_prompt_cached

VAR_RE = re.compile(r"\{\{(\w+)\}\}")

def load_prompt_uncached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def run_benchmark():
    iterations = 5000
    print(f"🚀 Running prompt loading benchmark ({iterations:,} iterations)...")

    # Warmup
    build_prompt("gem5", {"input": "warmup"})

    # Benchmark uncached template load
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt_uncached("gem5")
        load_prompt_uncached("00_prompt_maestro")
    uncached_duration = time.perf_counter() - start

    # Benchmark cached template load
    _load_prompt_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem5", {"input": "benchmark_data"})
    cached_duration = time.perf_counter() - start

    speedup = uncached_duration / cached_duration
    cache_info = _load_prompt_cached.cache_info()

    print(f"  ⏱️  Uncached direct file I/O: {uncached_duration:.4f}s")
    print(f"  ⚡ LRU Cached prompt build:   {cached_duration:.4f}s")
    print(f"  📈 Speedup:                   {speedup:.2f}x faster")
    print(f"  📊 Cache Info:                {cache_info}")

if __name__ == "__main__":
    run_benchmark()
