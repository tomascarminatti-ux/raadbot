"""
test_prompt_builder.py – Unit tests for agent/prompt_builder.py caching and template loading.
"""

import os
import pytest
from agent.prompt_builder import load_prompt, build_prompt, get_required_variables, _load_prompt_cached


def test_load_prompt_caching():
    _load_prompt_cached.cache_clear()
    info_before = _load_prompt_cached.cache_info()
    assert info_before.hits == 0

    # First load -> cache miss
    content1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.misses == 1

    # Second load -> cache hit
    content2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1
    assert content1 == content2


def test_cache_invalidation_on_mtime_change(tmp_path):
    _load_prompt_cached.cache_clear()
    test_file = tmp_path / "test_gem.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    filepath = str(test_file)
    mtime1 = os.path.getmtime(filepath)

    res1 = _load_prompt_cached(filepath, mtime1)
    assert res1 == "Hello {{name}}"

    # Modify file and update mtime using os.utime to avoid coarse timer issues
    test_file.write_text("Updated {{name}}", encoding="utf-8")
    mtime2 = mtime1 + 10.0
    os.utime(filepath, (mtime2, mtime2))

    res2 = _load_prompt_cached(filepath, mtime2)
    assert res2 == "Updated {{name}}"


def test_build_prompt_variable_replacement():
    prompt = build_prompt("gem1", {"candidate_id": "CAND123", "role": "Architect"})
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_get_required_variables():
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
    assert "PROMPT_MAESTRO" not in vars_list
    assert "VERSION" not in vars_list
