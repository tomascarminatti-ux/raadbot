import pytest
import os
import shutil
from agent.prompt_builder import load_prompt, clear_prompt_caches

def test_prompt_cache_and_invalidation():
    # Make sure cache is clean at start
    clear_prompt_caches()

    # Measure baseline: load "gem5" prompt
    content1 = load_prompt("gem5")
    assert content1 is not None
    assert len(content1) > 0

    # Try loading again (should be hit from cache)
    content2 = load_prompt("gem5")
    assert content1 == content2

    # Modify the prompt file on disk to test invalidation
    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    filepath = os.path.join(prompts_dir, "gem5.md")

    # Backup original content
    with open(filepath, "r", encoding="utf-8") as f:
        original_content = f.read()

    try:
        # Write modified content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("MODIFIED_PROMPT_CONTENT_FOR_TESTING")

        # Due to caching, loading "gem5" should still return original content
        cached_content = load_prompt("gem5")
        assert cached_content == content1
        assert cached_content != "MODIFIED_PROMPT_CONTENT_FOR_TESTING"

        # Explicitly clear the cache
        clear_prompt_caches()

        # Now, loading "gem5" must return the modified content
        fresh_content = load_prompt("gem5")
        assert fresh_content == "MODIFIED_PROMPT_CONTENT_FOR_TESTING"

    finally:
        # Restore original prompt content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(original_content)

        # Clear cache again
        clear_prompt_caches()

        # Verify original content is back
        restored_content = load_prompt("gem5")
        assert restored_content == original_content
