import os
import time
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR


def test_load_prompt_caching_and_invalidation():
    # Ensure cache is clear before test
    clear_prompt_caches()

    test_prompt_file = os.path.join(PROMPTS_DIR, "temp_test_prompt.md")
    try:
        # Create temporary prompt file
        with open(test_prompt_file, "w", encoding="utf-8") as f:
            f.write("Initial Content")

        # Initial load
        content1 = load_prompt("temp_test_prompt")
        assert content1 == "Initial Content"

        # Modify file on disk without clearing cache
        with open(test_prompt_file, "w", encoding="utf-8") as f:
            f.write("Updated Content")

        # Should still return cached initial content
        content_cached = load_prompt("temp_test_prompt")
        assert content_cached == "Initial Content"

        # Invalidate cache
        clear_prompt_caches()

        # Should now load updated content
        content_updated = load_prompt("temp_test_prompt")
        assert content_updated == "Updated Content"

    finally:
        if os.path.exists(test_prompt_file):
            os.remove(test_prompt_file)
        clear_prompt_caches()


def test_load_prompt_benchmark_speedup():
    clear_prompt_caches()
    # Benchmark caching speedup
    t0 = time.perf_counter()
    for _ in range(1000):
        load_prompt("gem1")
    t1 = time.perf_counter()

    duration = t1 - t0
    # 1000 cached loads should complete in under 0.05 seconds
    assert duration < 0.05
