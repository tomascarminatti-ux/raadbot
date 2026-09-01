import os
import time
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR


def test_prompt_builder_cache_hit_and_invalidation(tmp_path):
    # Setup temporary prompt file in PROMPTS_DIR
    temp_prompt_name = "test_temp_cache_prompt"
    temp_prompt_file = os.path.join(PROMPTS_DIR, f"{temp_prompt_name}.md")

    initial_content = "Hello {{candidate_name}}, initial version."
    updated_content = "Hello {{candidate_name}}, updated version."

    try:
        # Step 1: Write initial content and load
        with open(temp_prompt_file, "w", encoding="utf-8") as f:
            f.write(initial_content)

        clear_prompt_caches()

        content1 = load_prompt(temp_prompt_name)
        assert content1 == initial_content

        # Step 2: Modify file on disk without clearing cache
        with open(temp_prompt_file, "w", encoding="utf-8") as f:
            f.write(updated_content)

        content_cached = load_prompt(temp_prompt_name)
        assert content_cached == initial_content, "Expected cached content before cache invalidation"

        # Step 3: Invalidate cache and reload
        clear_prompt_caches()
        content_invalidated = load_prompt(temp_prompt_name)
        assert content_invalidated == updated_content, "Expected updated content after cache invalidation"

    finally:
        if os.path.exists(temp_prompt_file):
            os.remove(temp_prompt_file)
        clear_prompt_caches()


def test_prompt_builder_cache_performance():
    clear_prompt_caches()

    iterations = 1000

    # Warmup and verify cache hits counter
    load_prompt("00_prompt_maestro")
    initial_info = load_prompt.cache_info()

    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt("00_prompt_maestro")
    elapsed_cached = time.perf_counter() - start

    cached_info = load_prompt.cache_info()
    assert cached_info.hits >= initial_info.hits + iterations

    # Measure uncached by calling the unwrapped function
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt.__wrapped__("00_prompt_maestro")
    elapsed_uncached = time.perf_counter() - start

    speedup = elapsed_uncached / elapsed_cached if elapsed_cached > 0 else float("inf")
    print(f"\nCache benchmark: Uncached={elapsed_uncached:.4f}s, Cached={elapsed_cached:.4f}s, Speedup={speedup:.2f}x")
