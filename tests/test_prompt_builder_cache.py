import os
import time
from agent.prompt_builder import load_prompt, _load_prompt_cached, clear_prompt_caches, PROMPTS_DIR


def test_prompt_builder_cache_and_invalidation():
    temp_filename = "temp_test_prompt_cache.md"
    temp_filepath = os.path.join(PROMPTS_DIR, temp_filename)
    gem_name = "temp_test_prompt_cache"

    try:
        # Clear cache before starting
        clear_prompt_caches()
        initial_info = _load_prompt_cached.cache_info()

        # Write initial version
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Initial prompt content {{test_var}}")

        # First load - should be a cache miss
        content1 = load_prompt(gem_name)
        assert content1 == "Initial prompt content {{test_var}}"
        info1 = _load_prompt_cached.cache_info()
        assert info1.misses == initial_info.misses + 1

        # Second load without modifying file - should be a cache hit
        content2 = load_prompt(gem_name)
        assert content2 == "Initial prompt content {{test_var}}"
        info2 = _load_prompt_cached.cache_info()
        assert info2.hits == info1.hits + 1

        # Modify file and update mtime using os.utime to ensure instant invalidation
        time.sleep(0.01)
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Updated prompt content {{test_var}}")

        new_mtime = time.time() + 10.0
        os.utime(temp_filepath, (new_mtime, new_mtime))

        # Third load after mtime update - should be a cache miss and reflect updated content
        content3 = load_prompt(gem_name)
        assert content3 == "Updated prompt content {{test_var}}"
        info3 = _load_prompt_cached.cache_info()
        assert info3.misses == info2.misses + 1

    finally:
        clear_prompt_caches()
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
