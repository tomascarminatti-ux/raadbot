import os
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    build_agent_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_caching():
    _load_prompt_cached.cache_clear()
    info_start = _load_prompt_cached.cache_info()
    assert info_start.hits == 0

    content1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0

    content2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits >= 1
    assert content1 == content2


def test_build_agent_prompt_appends_data():
    payload = {"search_id": "SEARCH-123", "candidate_id": "CAND-456"}
    prompt = build_agent_prompt("gem5", payload)
    assert "### DATA INPUT:" in prompt
    assert "SEARCH-123" in prompt
    assert "CAND-456" in prompt


def test_get_required_variables():
    req_vars = get_required_variables("gem5")
    assert isinstance(req_vars, list)
    assert "PROMPT_MAESTRO" not in req_vars
    assert "VERSION" not in req_vars
