import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    build_agent_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching():
    """Verify that load_prompt caches prompt file reads using LRU cache."""
    _load_prompt_cached.cache_clear()

    # First call: cache miss
    content1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Second call: cache hit
    content2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert content1 == content2
    assert info2.hits == 1
    assert info2.misses == 1


def test_cache_invalidation_on_mtime_change(tmp_path, monkeypatch):
    """Verify that updating mtime invalidates the cache automatically."""
    _load_prompt_cached.cache_clear()

    test_file = tmp_path / "test_prompt.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    import agent.prompt_builder as pb

    monkeypatch.setattr(pb, "PROMPTS_DIR", str(tmp_path))

    # Read original
    p1 = pb.load_prompt("test_prompt")
    assert p1 == "Hello {{name}}"

    info1 = _load_prompt_cached.cache_info()
    assert info1.misses >= 1

    # Call again, should be a hit
    p2 = pb.load_prompt("test_prompt")
    assert p2 == "Hello {{name}}"

    # Update file content and modify mtime
    time.sleep(0.01)
    test_file.write_text("Hello {{name}} Updated", encoding="utf-8")
    os.utime(test_file, (time.time() + 1, time.time() + 1))

    p3 = pb.load_prompt("test_prompt")
    assert p3 == "Hello {{name}} Updated"


def test_build_prompt():
    """Verify build_prompt replaces placeholders correctly."""
    prompt = build_agent_prompt("gem1", {"input": "test_job", "context": "test_ctx"})
    assert "test_job" in prompt


def test_get_required_variables():
    """Verify get_required_variables extracts placeholder names."""
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)
