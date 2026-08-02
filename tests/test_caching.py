import json
import os
import time

from agent.prompt_builder import clear_prompt_caches, load_prompt
from utils.gem_core import _load_contract_cached, validate_contract


def test_prompt_caching_and_invalidation():
    """Verify that prompt templates are cached and correctly invalidated when the file is modified."""
    temp_prompt_name = "temp_test_prompt"
    temp_prompt_path = os.path.join("prompts", f"{temp_prompt_name}.md")

    # Ensure prompts folder exists
    os.makedirs("prompts", exist_ok=True)

    # Write initial prompt
    with open(temp_prompt_path, "w", encoding="utf-8") as f:
        f.write("Initial Prompt Content")

    try:
        # Clear cache first to ensure a clean state
        clear_prompt_caches()

        # First load (Disk read)
        content_1 = load_prompt(temp_prompt_name)
        assert content_1 == "Initial Prompt Content"

        # Second load (Cached)
        content_2 = load_prompt(temp_prompt_name)
        assert content_2 == "Initial Prompt Content"

        # Modify the prompt file on disk
        with open(temp_prompt_path, "w", encoding="utf-8") as f:
            f.write("Modified Prompt Content")

        # Explicitly modify utime to guarantee mtime resolution changes (some filesystems have coarse resolution)
        current_mtime = os.path.getmtime(temp_prompt_path)
        os.utime(temp_prompt_path, (current_mtime + 5, current_mtime + 5))

        # Load again - should detect modification and load the modified content
        content_3 = load_prompt(temp_prompt_name)
        assert content_3 == "Modified Prompt Content"

    finally:
        # Cleanup
        if os.path.exists(temp_prompt_path):
            os.remove(temp_prompt_path)

        clear_prompt_caches()


def test_contract_caching_and_invalidation():
    """Verify that contract schemas are cached and correctly invalidated when modified on disk."""
    temp_contract_path = os.path.join("contracts", "temp_test_contract.json")

    # Ensure contracts folder exists
    os.makedirs("contracts", exist_ok=True)

    # Write initial contract schema
    contract_schema = {"score": "number", "name": "string"}
    with open(temp_contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_schema, f)

    try:
        # Clear cache by clearing lru_cache
        _load_contract_cached.cache_clear()

        # Validate data
        data = {"score": 9.5, "name": "Test User"}
        assert validate_contract(data, temp_contract_path) is True

        # Modify the schema file on disk
        modified_schema = {
            "score": "number",
            "name": "string",
            "required_field": "boolean",
        }
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            json.dump(modified_schema, f)

        current_mtime = os.path.getmtime(temp_contract_path)
        os.utime(temp_contract_path, (current_mtime + 5, current_mtime + 5))

        # Validation with old data should now FAIL because "required_field" is missing
        assert validate_contract(data, temp_contract_path) is False

        # Validation with correct data should pass
        correct_data = {"score": 9.5, "name": "Test User", "required_field": True}
        assert validate_contract(correct_data, temp_contract_path) is True

    finally:
        # Cleanup
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)
        _load_contract_cached.cache_clear()


def test_performance_benchmark():
    """Benchmark the performance improvement of using cached loading vs raw disk loading."""
    temp_prompt_name = "temp_perf_test_prompt"
    temp_prompt_path = os.path.join("prompts", f"{temp_prompt_name}.md")

    os.makedirs("prompts", exist_ok=True)
    with open(temp_prompt_path, "w", encoding="utf-8") as f:
        f.write("A repetitive template to benchmark performance metrics " * 10)

    try:
        # Raw disk reading function for comparison
        def load_raw_disk():
            with open(temp_prompt_path, "r", encoding="utf-8") as f:
                return f.read()

        # Warmup and clear caches
        clear_prompt_caches()

        # Benchmark Raw Disk Reading
        start_time = time.perf_counter()
        for _ in range(1000):
            _ = load_raw_disk()
        raw_duration = time.perf_counter() - start_time

        # Benchmark Cached Reading
        start_time = time.perf_counter()
        for _ in range(1000):
            _ = load_prompt(temp_prompt_name)
        cached_duration = time.perf_counter() - start_time

        speedup = raw_duration / cached_duration if cached_duration > 0 else 0

        print("\n--- Benchmark Results ---")
        print(f"Raw Disk Duration (1000 iterations): {raw_duration:.5f}s")
        print(f"Cached Duration (1000 iterations):   {cached_duration:.5f}s")
        print(f"Calculated Speedup Factor:            {speedup:.2f}x")
        print("--------------------------")

        # Caching should be significantly faster (at least 2x faster, usually >5x faster)
        assert speedup > 2.0 or cached_duration < 0.05

    finally:
        if os.path.exists(temp_prompt_path):
            os.remove(temp_prompt_path)
        clear_prompt_caches()
