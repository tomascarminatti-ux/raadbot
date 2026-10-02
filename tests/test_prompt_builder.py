import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt():
    content = load_prompt("gem1")
    assert "PROMPT_MAESTRO" in content or "VERSION" in content or len(content) > 0


def test_load_prompt_not_found():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")


def test_load_prompt_caching(tmp_path, monkeypatch):
    test_prompts_dir = tmp_path / "prompts"
    test_prompts_dir.mkdir()
    prompt_file = test_prompts_dir / "test_gem.md"
    prompt_file.write_text("Hello {{name}}!", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(test_prompts_dir))
    _load_prompt_cached.cache_clear()

    initial_info = _load_prompt_cached.cache_info()
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}!"

    content2 = load_prompt("test_gem")
    assert content2 == "Hello {{name}}!"

    info_after = _load_prompt_cached.cache_info()
    assert info_after.hits > initial_info.hits


def test_load_prompt_cache_invalidation(tmp_path, monkeypatch):
    test_prompts_dir = tmp_path / "prompts"
    test_prompts_dir.mkdir()
    prompt_file = test_prompts_dir / "test_gem_inv.md"
    prompt_file.write_text("Version 1", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(test_prompts_dir))
    _load_prompt_cached.cache_clear()

    assert load_prompt("test_gem_inv") == "Version 1"

    # Sleep slightly to guarantee updated mtime timestamp
    time.sleep(0.05)
    prompt_file.write_text("Version 2 Updated", encoding="utf-8")

    assert load_prompt("test_gem_inv") == "Version 2 Updated"


def test_build_prompt():
    _load_prompt_cached.cache_clear()
    vars_dict = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV",
        "interview_notes": "Sample Notes",
        "gem5_summary": "Sample Gem5 Summary",
    }
    built = build_prompt("gem1", vars_dict)
    assert "SEARCH-001" in built
    assert "CAND-001" in built
    assert "Sample CV" in built


def test_get_required_variables():
    req_vars = get_required_variables("gem1")
    assert "candidate_id" in req_vars or "cv_text" in req_vars
    assert "PROMPT_MAESTRO" not in req_vars
    assert "VERSION" not in req_vars
