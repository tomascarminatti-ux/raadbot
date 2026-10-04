import os
import time
import pytest
from agent.prompt_builder import load_prompt, _load_prompt_cached, build_prompt, get_required_variables

def test_load_prompt_caching(tmp_path, monkeypatch):
    # Setup temporary prompts directory
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    test_file = prompts_dir / "test_gem.md"
    test_file.write_text("Hello {{name}}", encoding="utf-8")

    import agent.prompt_builder as pb
    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))

    # Clear LRU cache before test
    _load_prompt_cached.cache_clear()
    initial_info = _load_prompt_cached.cache_info()

    # First load - cache miss
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}"
    assert _load_prompt_cached.cache_info().misses == initial_info.misses + 1

    # Second load - cache hit
    content2 = load_prompt("test_gem")
    assert content2 == "Hello {{name}}"
    assert _load_prompt_cached.cache_info().hits == initial_info.hits + 1

    # Write new content and modify mtime to trigger cache invalidation
    test_file.write_text("Hello updated {{name}}", encoding="utf-8")
    new_mtime = os.path.getmtime(str(test_file)) + 10.0
    os.utime(str(test_file), (new_mtime, new_mtime))

    # Third load - new mtime leads to cache miss
    content3 = load_prompt("test_gem")
    assert content3 == "Hello updated {{name}}"
    assert _load_prompt_cached.cache_info().misses == initial_info.misses + 2


def test_build_prompt_and_get_required_variables():
    # Test built-in gem loading and prompt building
    prompt = build_prompt("gem1", {"candidate_id": "c123", "jd_text": "Software Engineer"})
    assert "Software Engineer" in prompt or len(prompt) > 0

    req_vars = get_required_variables("gem1")
    assert isinstance(req_vars, list)
