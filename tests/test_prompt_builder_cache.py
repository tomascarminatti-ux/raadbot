import pytest
import os
from agent.prompt_builder import load_prompt, clear_prompt_caches

def test_prompt_cache_and_invalidation():
    # Make sure cache is clean at start
    clear_prompt_caches()

    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    filepath = os.path.join(prompts_dir, "temp_test_prompt.md")

    # Write a temporary prompt file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("ORIGINAL_PROMPT_CONTENT_FOR_TESTING")

    try:
        # Load the temporary prompt (should read from disk first time)
        content1 = load_prompt("temp_test_prompt")
        assert content1 == "ORIGINAL_PROMPT_CONTENT_FOR_TESTING"

        # Modify the prompt file on disk
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("MODIFIED_PROMPT_CONTENT_FOR_TESTING")

        # Due to caching, loading "temp_test_prompt" should still return original cached content
        cached_content = load_prompt("temp_test_prompt")
        assert cached_content == "ORIGINAL_PROMPT_CONTENT_FOR_TESTING"

        # Explicitly clear the cache
        clear_prompt_caches()

        # Now, loading "temp_test_prompt" must return the modified content
        fresh_content = load_prompt("temp_test_prompt")
        assert fresh_content == "MODIFIED_PROMPT_CONTENT_FOR_TESTING"

    finally:
        # Clean up the temporary file from disk
        if os.path.exists(filepath):
            os.remove(filepath)

        # Clear cache again so no remnants are left in memory
        clear_prompt_caches()

    # Verify that file not found is raised correctly
    with pytest.raises(FileNotFoundError):
        load_prompt("temp_test_prompt")
