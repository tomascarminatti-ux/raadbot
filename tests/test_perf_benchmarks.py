import time
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_cache


def test_prompt_loading_cache_performance():
    """Benchmark comparing cached prompt template loading versus uncached template loading."""
    target_prompt = "00_prompt_maestro"
    # Warm up
    load_prompt(target_prompt)

    # 1. Benchmark cached loading
    start_cached = time.perf_counter()
    for _ in range(200):
        # This will hit the lru_cache
        load_prompt(target_prompt)
    end_cached = time.perf_counter()
    cached_duration = end_cached - start_cached

    # 2. Benchmark uncached loading (by clearing cache on every iteration)
    start_uncached = time.perf_counter()
    for _ in range(200):
        clear_prompt_cache()
        load_prompt(target_prompt)
    end_uncached = time.perf_counter()
    uncached_duration = end_uncached - start_uncached

    speedup = uncached_duration / cached_duration
    print(f"\n⚡ Performance Benchmark Result:")
    print(f"   Uncached duration (200 loads): {uncached_duration:.6f}s")
    print(f"   Cached duration (200 loads):   {cached_duration:.6f}s")
    print(f"   Speedup factor:                {speedup:.2f}x faster!")

    # Verify correctness and speedup
    assert cached_duration < uncached_duration
    assert speedup > 2.0  # Safe threshold, usually 20x to 100x+ faster
