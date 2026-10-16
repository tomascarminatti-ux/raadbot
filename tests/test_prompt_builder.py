import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached
)


def test_prompt_builder_cache_and_invalidation(tmp_path, monkeypatch):
    """Test that _load_prompt_cached caches results and invalidates when mtime changes."""
    # Create temporary prompt directory and file
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "test_gem.md"
    prompt_file.write_text("Hello {{name}}", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    # Initial load should be a cache miss
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}"
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Second load should hit the cache
    content2 = load_prompt("test_gem")
    assert content2 == "Hello {{name}}"
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1

    # Update file content and mtime
    time.sleep(0.01)  # Ensure mtime difference
    prompt_file.write_text("Updated {{name}}", encoding="utf-8")
    os.utime(str(prompt_file), None)

    # Load after file update should fetch updated content (cache miss on new mtime key)
    content3 = load_prompt("test_gem")
    assert content3 == "Updated {{name}}"
    info3 = _load_prompt_cached.cache_info()
    assert info3.misses == 2


def test_build_prompt_placeholder_replacement(tmp_path, monkeypatch):
    """Test building prompt with variable replacement."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "00_prompt_maestro.md").write_text("MAESTRO_CONTENT", encoding="utf-8")
    (prompts_dir / "gem_test.md").write_text("{{PROMPT_MAESTRO}} | Hello {{name}}", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    prompt = build_prompt("gem_test", {"name": "Alice"})
    assert "MAESTRO_CONTENT" in prompt
    assert "Hello Alice" in prompt


def test_get_required_variables():
    """Test required variable extraction from prompt."""
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
    assert "PROMPT_MAESTRO" not in vars_list
    assert "VERSION" not in vars_list
