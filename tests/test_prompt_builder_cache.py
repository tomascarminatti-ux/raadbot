"""
test_prompt_builder_cache.py – Unit tests for prompt builder LRU caching and prompt building.
"""

from agent.prompt_builder import (
    load_prompt,
    clear_prompt_caches,
    build_prompt,
    get_required_variables,
)


def test_prompt_builder_lru_cache():
    clear_prompt_caches()

    # Initial call populates the cache
    prompt_1 = load_prompt("00_prompt_maestro")
    info_1 = load_prompt.cache_info()
    hits_before = info_1.hits
    misses_before = info_1.misses

    # Second call should hit the cache
    prompt_2 = load_prompt("00_prompt_maestro")
    info_2 = load_prompt.cache_info()

    assert prompt_1 == prompt_2
    assert info_2.hits == hits_before + 1
    assert info_2.misses == misses_before

    # Clear cache and verify miss on subsequent load
    clear_prompt_caches()
    info_3 = load_prompt.cache_info()
    assert info_3.hits == 0
    assert info_3.misses == 0


def test_build_prompt_formatting():
    clear_prompt_caches()
    variables = {
        "search_id": "TEST_SEARCH_01",
        "jd_text": "Software Engineer JD",
        "kickoff_notes": "Kickoff notes text",
        "company_context": "Company context text",
        "client_culture": "Culture text",
    }
    prompt = build_prompt("gem5", variables)
    assert "TEST_SEARCH_01" in prompt
    assert "Software Engineer JD" in prompt
    assert "{{search_id}}" not in prompt


def test_get_required_variables():
    vars_gem5 = get_required_variables("gem5")
    assert isinstance(vars_gem5, list)
    assert "search_id" in vars_gem5
    assert "PROMPT_MAESTRO" not in vars_gem5
