import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching(tmp_path, monkeypatch):
    prompt_file = tmp_path / "test_gem.md"
    prompt_file.write_text("Hello {{name}}!", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))

    # Initial cache info
    _load_prompt_cached.cache_clear()
    initial_info = _load_prompt_cached.cache_info()

    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}!"

    # Second call should hit LRU cache because mtime is identical
    content2 = load_prompt("test_gem")
    assert content2 == "Hello {{name}}!"
    info = _load_prompt_cached.cache_info()
    assert info.hits == initial_info.hits + 1

    # Update file content and mtime
    time.sleep(0.01)
    prompt_file.write_text("Updated {{name}}!", encoding="utf-8")
    new_mtime = os.path.getmtime(str(prompt_file)) + 1.0
    os.utime(str(prompt_file), (new_mtime, new_mtime))

    content3 = load_prompt("test_gem")
    assert content3 == "Updated {{name}}!"


def test_load_prompt_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")


def test_build_prompt():
    prompt = build_prompt("gem1", {"search_id": "S1", "candidate_id": "C1", "cv_text": "CV Data"})
    assert "S1" in prompt
    assert "C1" in prompt
    assert "CV Data" in prompt


def test_get_required_variables():
    vars_gem1 = get_required_variables("gem1")
    assert "search_id" in vars_gem1
    assert "candidate_id" in vars_gem1
    assert "PROMPT_MAESTRO" not in vars_gem1
    assert "VERSION" not in vars_gem1
