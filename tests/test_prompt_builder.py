import pytest
from agent.prompt_builder import load_prompt, build_prompt, get_required_variables


def test_load_prompt_caching():
    load_prompt.cache_clear()
    info0 = load_prompt.cache_info()

    p1 = load_prompt("gem1")
    info1 = load_prompt.cache_info()
    assert info1.hits == info0.hits
    assert info1.misses == info0.misses + 1

    p2 = load_prompt("gem1")
    info2 = load_prompt.cache_info()
    assert info2.hits == info1.hits + 1
    assert p1 == p2

    load_prompt.cache_clear()
    info3 = load_prompt.cache_info()
    assert info3.hits == 0
    assert info3.misses == 0


def test_build_prompt():
    load_prompt.cache_clear()
    prompt = build_prompt(
        "gem5",
        {
            "search_id": "TEST-123",
            "jd_text": "Sample JD",
            "kickoff_notes": "Sample Notes",
            "company_context": "Sample Context",
            "client_culture": "Sample Culture",
        },
    )

    assert isinstance(prompt, str)
    assert "TEST-123" in prompt
    assert "Sample JD" in prompt


def test_get_required_variables():
    vars_gem1 = get_required_variables("gem1")
    assert isinstance(vars_gem1, list)
    assert "PROMPT_MAESTRO" not in vars_gem1
    assert "VERSION" not in vars_gem1
