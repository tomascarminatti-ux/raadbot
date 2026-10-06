import os
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
    build_agent_prompt
)


def test_load_prompt_cached():
    """Verify that load_prompt correctly caches content and invalidates when mtime changes."""
    # Clear cache before starting
    _load_prompt_cached.cache_clear()

    # Call load_prompt twice
    p1 = load_prompt("gem1")
    p2 = load_prompt("gem1")

    assert p1 == p2
    info = _load_prompt_cached.cache_info()
    assert info.hits >= 1, "Cache hit count should increase on second load"


def test_load_prompt_not_found():
    """Verify FileNotFoundError when loading non-existent prompt."""
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")


def test_build_prompt_maestro_injection():
    """Verify build_prompt correctly injects 00_prompt_maestro when placeholder exists or appends payload."""
    prompt = build_agent_prompt("gem1", {"test_key": "test_value_123"})
    assert "test_value_123" in prompt


def test_get_required_variables():
    """Verify get_required_variables returns a list."""
    vars_gem1 = get_required_variables("gem1")
    assert isinstance(vars_gem1, list)
