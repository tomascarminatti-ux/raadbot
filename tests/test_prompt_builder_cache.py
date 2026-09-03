import os
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR

def test_load_prompt_lru_cache_and_invalidation(tmp_path, monkeypatch):
    # Setup temporary prompt file in tmp_path
    prompt_file = tmp_path / "temp_test_gem.md"
    prompt_file.write_text("Prompt version 1", encoding="utf-8")

    # Point PROMPTS_DIR to tmp_path
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))

    # Clear cache before starting
    clear_prompt_caches()

    # First call reads from disk and populates cache
    content1 = load_prompt("temp_test_gem")
    assert content1 == "Prompt version 1"

    # Modify file on disk
    prompt_file.write_text("Prompt version 2", encoding="utf-8")

    # Second call should return cached version 1
    content2 = load_prompt("temp_test_gem")
    assert content2 == "Prompt version 1"

    # Clear prompt cache
    clear_prompt_caches()

    # Third call after cache clear should read updated version 2 from disk
    content3 = load_prompt("temp_test_gem")
    assert content3 == "Prompt version 2"
