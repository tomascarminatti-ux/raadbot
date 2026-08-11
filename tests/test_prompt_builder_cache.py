import os
import time
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR


def test_prompt_cache_correctness_and_invalidation():
    # Setup a temporary prompt file
    temp_name = "temp_test_cache_prompt"
    temp_path = os.path.join(PROMPTS_DIR, f"{temp_name}.md")

    try:
        # 1. Write initial content
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write("Initial Content")

        # Ensure cache starts clear
        clear_prompt_caches()

        # 2. First load should read from disk
        content1 = load_prompt(temp_name)
        assert content1 == "Initial Content"

        # 3. Change content on disk (without clearing cache)
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write("Modified Content")

        # 4. Loading again should return the CACHED (initial) content
        content2 = load_prompt(temp_name)
        assert content2 == "Initial Content"

        # 5. Clear cache
        clear_prompt_caches()

        # 6. Loading now should return the NEW content from disk
        content3 = load_prompt(temp_name)
        assert content3 == "Modified Content"

    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
        clear_prompt_caches()


def test_prompt_cache_performance():
    # Ensure cache is filled
    clear_prompt_caches()
    # We load "gem1" once to populate cache
    load_prompt("gem1")

    # Measure cached loads
    start_cached = time.perf_counter()
    for _ in range(1000):
        load_prompt("gem1")
    elapsed_cached = time.perf_counter() - start_cached

    # Measure uncached loads by clearing the cache every time
    start_uncached = time.perf_counter()
    for _ in range(1000):
        clear_prompt_caches()
        load_prompt("gem1")
    elapsed_uncached = time.perf_counter() - start_uncached

    print(f"\n[BENCHMARK] 1000 cached loads: {elapsed_cached:.6f}s")
    print(f"[BENCHMARK] 1000 uncached loads: {elapsed_uncached:.6f}s")

    # Cached should be significantly faster (usually > 4x speedup)
    assert elapsed_cached < elapsed_uncached
