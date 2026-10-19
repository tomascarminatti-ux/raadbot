import pytest
import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    load_maestro,
    _load_prompt_cached,
)


def test_load_prompt():
    prompt = load_prompt("gem1")
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_load_prompt_caching():
    # Cache hit check
    info_before = _load_prompt_cached.cache_info()
    _ = load_prompt("gem1")
    _ = load_prompt("gem1")
    info_after = _load_prompt_cached.cache_info()

    assert info_after.hits > info_before.hits


def test_load_prompt_invalidation(tmp_path, monkeypatch):
    import agent.prompt_builder as pb

    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    test_file = prompts_dir / "test_gem.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))

    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}"

    # Update file content and mtime
    time.sleep(0.01)
    test_file.write_text("Updated {{name}}", encoding="utf-8")

    content2 = load_prompt("test_gem")
    assert content2 == "Updated {{name}}"


def test_load_maestro():
    maestro = load_maestro()
    assert isinstance(maestro, str)
    assert len(maestro) > 0


def test_build_prompt():
    vars = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV text",
        "interview_notes": "Sample notes",
        "gem5_summary": "Sample summary",
    }
    prompt = build_prompt("gem1", vars)
    assert "SEARCH-001" in prompt
    assert "CAND-001" in prompt
    assert "Sample CV text" in prompt


def test_get_required_variables():
    vars = get_required_variables("gem1")
    assert isinstance(vars, list)
    assert "cv_text" in vars
