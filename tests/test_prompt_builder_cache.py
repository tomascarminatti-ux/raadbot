import os
import tempfile
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR

def test_prompt_caching_and_invalidation():
    # Ensure cache is clear initially
    clear_prompt_caches()

    # Create a temporary prompt file in PROMPTS_DIR
    temp_filename = "temp_test_prompt"
    temp_filepath = os.path.join(PROMPTS_DIR, f"{temp_filename}.md")

    try:
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Initial prompt content")

        # First call loads from file and caches
        content1 = load_prompt(temp_filename)
        assert content1 == "Initial prompt content"

        # Modify the file on disk
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Updated prompt content")

        # Call again without clearing cache -> should return cached content
        content2 = load_prompt(temp_filename)
        assert content2 == "Initial prompt content"

        # Clear cache
        clear_prompt_caches()

        # Call after clearing cache -> should return updated content
        content3 = load_prompt(temp_filename)
        assert content3 == "Updated prompt content"

    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        clear_prompt_caches()
