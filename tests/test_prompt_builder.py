import pytest
import os
import time
from agent.prompt_builder import load_prompt, build_prompt, get_required_variables, _load_prompt_cached

def test_prompt_builder_cache_and_building():
    # Clear cache first
    _load_prompt_cached.cache_clear()
    info0 = _load_prompt_cached.cache_info()

    # First call - cache miss
    p1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.misses == info0.misses + 1

    # Second call - cache hit
    p2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == info1.hits + 1
    assert p1 == p2

    # Verify build_prompt
    vars_dict = {
        "search_id": "TEST-123",
        "input": {"data": "test_input"}
    }
    built = build_prompt("gem1", vars_dict)
    assert isinstance(built, str)
    assert len(built) > 0
    assert "{{PROMPT_MAESTRO}}" not in built

def test_get_required_variables():
    req_vars = get_required_variables("gem1")
    assert isinstance(req_vars, list)
    assert "PROMPT_MAESTRO" not in req_vars
    assert "VERSION" not in req_vars
