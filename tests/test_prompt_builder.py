import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_existing():
    prompt = load_prompt("gem1")
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_load_prompt_non_existent():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")


def test_prompt_builder_cache_and_invalidation(tmp_path, monkeypatch):
    test_prompt_file = tmp_path / "test_gem.md"
    test_prompt_file.write_text("Hello {{name}}! Version {{VERSION}}", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))

    # Clear cache before test
    _load_prompt_cached.cache_clear()

    # Initial load
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}! Version {{VERSION}}"
    cache_info1 = _load_prompt_cached.cache_info()

    # Second load should hit cache
    content2 = load_prompt("test_gem")
    assert content2 == content1
    cache_info2 = _load_prompt_cached.cache_info()
    assert cache_info2.hits == cache_info1.hits + 1

    # Update file text first, then explicitly set new mtime
    test_prompt_file.write_text("Updated {{name}}!", encoding="utf-8")
    new_mtime = time.time() + 10
    os.utime(test_prompt_file, (new_mtime, new_mtime))

    # Third load should miss cache due to updated mtime
    content3 = load_prompt("test_gem")
    assert content3 == "Updated {{name}}!"
    cache_info3 = _load_prompt_cached.cache_info()
    assert cache_info3.misses == cache_info1.misses + 1


def test_build_prompt_variable_substitution():
    prompt = build_prompt("gem1", {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV",
        "interview_notes": "Sample Notes",
        "gem5_summary": {"key": "val"},
    })
    assert "SEARCH-001" in prompt
    assert "CAND-001" in prompt
    assert '"key": "val"' in prompt
    assert "{{search_id}}" not in prompt


def test_get_required_variables():
    vars = get_required_variables("gem1")
    assert "search_id" in vars
    assert "candidate_id" in vars
    assert "PROMPT_MAESTRO" not in vars
    assert "VERSION" not in vars
