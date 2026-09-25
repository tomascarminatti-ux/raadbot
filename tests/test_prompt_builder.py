import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching():
    # Clear cache before test
    _load_prompt_cached.cache_clear()

    content = load_prompt("gem1")
    assert content is not None
    assert isinstance(content, str)

    info1 = _load_prompt_cached.cache_info()

    # Second call should result in cache hit
    load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()

    assert info2.hits == info1.hits + 1


def test_cache_invalidation_on_mtime_change(tmp_path, monkeypatch):
    from agent import prompt_builder

    _load_prompt_cached.cache_clear()

    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "test_gem.md"
    prompt_file.write_text("Hello {{name}}", encoding="utf-8")

    monkeypatch.setattr(prompt_builder, "PROMPTS_DIR", str(prompts_dir))

    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}"

    info1 = _load_prompt_cached.cache_info()

    # Update file content and mtime
    new_mtime = time.time() + 10
    prompt_file.write_text("Updated {{name}}", encoding="utf-8")
    os.utime(str(prompt_file), (new_mtime, new_mtime))

    content2 = load_prompt("test_gem")
    assert content2 == "Updated {{name}}"

    info2 = _load_prompt_cached.cache_info()
    assert info2.misses == info1.misses + 1


def test_build_prompt():
    res = build_prompt(
        "gem1",
        {
            "search_id": "SEARCH-101",
            "candidate_id": "CAND-202",
            "cv_text": "Experienced Dev",
            "interview_notes": "Great fit",
            "gem5_summary": {"key": "val"},
        },
    )
    assert "SEARCH-101" in res
    assert "CAND-202" in res
    assert '"key": "val"' in res


def test_get_required_variables():
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
    assert "PROMPT_MAESTRO" not in vars_list
    assert "VERSION" not in vars_list


def test_load_prompt_not_found():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")
