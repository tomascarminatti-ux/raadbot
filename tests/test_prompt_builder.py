import pytest
from agent.prompt_builder import load_prompt, _load_prompt_cached, build_prompt


def test_prompt_loader_caching():
    _load_prompt_cached.cache_clear()

    # First call - cache miss
    p1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.misses == 1
    assert info1.hits == 0

    # Second call - cache hit
    p2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert info2.misses == 1
    assert info2.hits == 1
    assert p1 == p2


def test_build_prompt():
    prompt = build_prompt("gem1", {"search_id": "test_search"})
    assert isinstance(prompt, str)
    assert len(prompt) > 0
