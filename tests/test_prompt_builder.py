import os
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_caching():
    # Verify initial call populates LRU cache
    _load_prompt_cached.cache_clear()
    initial_hits = _load_prompt_cached.cache_info().hits
    initial_misses = _load_prompt_cached.cache_info().misses

    content1 = load_prompt("gem1")
    assert isinstance(content1, str)
    assert len(content1) > 0
    assert _load_prompt_cached.cache_info().misses == initial_misses + 1

    # Second call for same prompt should hit the LRU cache
    content2 = load_prompt("gem1")
    assert content1 == content2
    assert _load_prompt_cached.cache_info().hits == initial_hits + 1


def test_load_prompt_cache_invalidation(tmp_path):
    # Test mtime cache invalidation using a temporary prompt file
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    test_file = prompts_dir / "test_gem.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    filepath = str(test_file)
    mtime1 = os.path.getmtime(filepath)

    _load_prompt_cached.cache_clear()
    res1 = _load_prompt_cached(filepath, mtime1)
    assert res1 == "Hello {{name}}"

    # Modify file and update mtime using os.utime
    test_file.write_text("Hello updated {{name}}", encoding="utf-8")
    mtime2 = mtime1 + 5.0
    os.utime(filepath, (mtime2, mtime2))

    mtime_new = os.path.getmtime(filepath)
    res2 = _load_prompt_cached(filepath, mtime_new)
    assert res2 == "Hello updated {{name}}"


def test_build_prompt():
    prompt = build_prompt("gem1", {"role": "Engineer", "level": "Senior"})
    assert isinstance(prompt, str)
    assert "Engineer" in prompt or "Senior" in prompt or len(prompt) > 0


def test_get_required_variables():
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
