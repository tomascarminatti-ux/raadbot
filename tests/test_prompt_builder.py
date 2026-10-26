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

    # Initial load
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}!"

    # Cache hit info
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits + info1.misses > 0

    # Second load should hit cache
    content2 = load_prompt("test_gem")
    assert content2 == "Hello {{name}}!"
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits > info1.hits

    # Update file content and mtime
    time.sleep(0.01)
    prompt_file.write_text("Hello updated {{name}}!", encoding="utf-8")
    now = time.time() + 1
    os.utime(prompt_file, (now, now))

    content3 = load_prompt("test_gem")
    assert content3 == "Hello updated {{name}}!"


def test_build_prompt():
    vars_gem1 = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced Dev",
        "interview_notes": "Great interview",
        "gem5_summary": "Solid company fit",
    }
    prompt = build_prompt("gem1", vars_gem1)
    assert "SEARCH-001" in prompt
    assert "CAND-001" in prompt
    assert "Experienced Dev" in prompt


def test_get_required_variables():
    vars_req = get_required_variables("gem1")
    assert "cv_text" in vars_req
    assert "PROMPT_MAESTRO" not in vars_req


def test_load_prompt_nonexistent():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")
