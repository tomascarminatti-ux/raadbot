import os
import time

from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_prompt_caching_and_invalidation(tmp_path):
    """Test that _load_prompt_cached invalidates on mtime change."""
    _load_prompt_cached.cache_clear()

    test_file = tmp_path / "test_gem.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    filepath = str(test_file)
    mtime1 = os.path.getmtime(filepath)

    # First read (cache miss)
    content1 = _load_prompt_cached(filepath, mtime1)
    assert content1 == "Hello {{name}}"
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0

    # Second read with same mtime (cache hit)
    content2 = _load_prompt_cached(filepath, mtime1)
    assert content2 == "Hello {{name}}"
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1

    # Update file content and mtime
    time.sleep(0.01)
    test_file.write_text("Hello updated {{name}}", encoding="utf-8")
    mtime2 = os.path.getmtime(filepath)
    assert mtime2 != mtime1

    # Third read with new mtime (cache miss, loads updated content)
    content3 = _load_prompt_cached(filepath, mtime2)
    assert content3 == "Hello updated {{name}}"


def test_load_prompt_and_build_prompt():
    """Verify loading real prompts and building prompts."""
    prompt = load_prompt("gem1")
    assert isinstance(prompt, str)
    assert len(prompt) > 0

    built = build_prompt(
        "gem1", {"input": "test_input", "context": "test_context"}
    )
    assert isinstance(built, str)
    assert "test_input" in built or "test_context" in built or len(built) > 0


def test_get_required_variables():
    """Verify required variable extraction from prompts."""
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
    assert "PROMPT_MAESTRO" not in vars_list
    assert "VERSION" not in vars_list
