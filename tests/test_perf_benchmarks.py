"""
tests/test_perf_benchmarks.py – Test suite and benchmarks for evaluating prompt builder performance.
"""

import os
import time
import pytest
from agent.prompt_builder import build_prompt, clear_prompt_caches, load_prompt, load_maestro

def test_prompt_builder_cache_behavior():
    # Load and build first time
    clear_prompt_caches()

    # Check cache info before
    info_before_prompt = load_prompt.cache_info()
    info_before_maestro = load_maestro.cache_info()

    variables = {
        "kickoff_notes": "Kickoff notes test content",
        "brief_jd": "JD test content",
        "company_context": "Company context content"
    }

    # 1. First run (misses)
    out1 = build_prompt("gem5", {"input": variables})

    # Cache info after first run
    info_after1_prompt = load_prompt.cache_info()
    info_after1_maestro = load_maestro.cache_info()

    assert info_after1_prompt.hits == info_before_prompt.hits
    assert info_after1_prompt.misses > info_before_prompt.misses
    assert info_after1_maestro.misses > info_before_maestro.misses

    # 2. Second run (hits)
    out2 = build_prompt("gem5", {"input": variables})

    # Both runs must yield identical outputs
    assert out1 == out2

    info_after2_prompt = load_prompt.cache_info()
    info_after2_maestro = load_maestro.cache_info()

    assert info_after2_prompt.hits > info_after1_prompt.hits
    assert info_after2_maestro.hits > info_after1_maestro.hits

    # 3. Clear cache
    clear_prompt_caches()
    info_after_clear_prompt = load_prompt.cache_info()
    assert info_after_clear_prompt.hits == 0
    assert info_after_clear_prompt.misses == 0


def test_prompt_builder_performance_gain():
    print("\n--- ⚡ Benchmarking Prompt Builder Performance ⚡ ---")

    variables = {
        "kickoff_notes": "Kickoff notes test content " * 10,
        "brief_jd": "JD test content " * 10,
        "company_context": "Company context content " * 10
    }

    # Measure uncached execution time (simulated by clearing cache on each iteration)
    iterations = 200
    start_uncached = time.perf_counter()
    for _ in range(iterations):
        clear_prompt_caches()
        build_prompt("gem5", {"input": variables})
    end_uncached = time.perf_counter()
    uncached_time = end_uncached - start_uncached
    uncached_avg_ms = (uncached_time / iterations) * 1000

    # Measure cached execution time
    clear_prompt_caches()
    # Warm up cache
    build_prompt("gem5", {"input": variables})

    start_cached = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem5", {"input": variables})
    end_cached = time.perf_counter()
    cached_time = end_cached - start_cached
    cached_avg_ms = (cached_time / iterations) * 1000

    speedup = uncached_avg_ms / cached_avg_ms if cached_avg_ms > 0 else 1.0
    print(f"Uncached (Disk + Re-parse) average time: {uncached_avg_ms:.4f} ms")
    print(f"Cached (LRU Cache) average time:         {cached_avg_ms:.4f} ms")
    print(f"⚡ Performance gain: {speedup:.2f}x faster!")

    # We expect a significant speedup (at least 1.5x)
    assert speedup >= 1.5
