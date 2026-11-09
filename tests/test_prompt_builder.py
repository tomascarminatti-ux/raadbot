import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_caching():
    # Clear cache before testing
    _load_prompt_cached.cache_clear()
    initial_info = _load_prompt_cached.cache_info()
    assert initial_info.currsize == 0

    # First load - cache miss
    content1 = load_prompt("gem1")
    info1 = _load_prompt_cached.cache_info()
    assert info1.misses >= 1
    assert info1.currsize >= 1

    # Second load - cache hit
    content2 = load_prompt("gem1")
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits >= 1
    assert content1 == content2


def test_load_prompt_not_found():
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")


def test_build_prompt():
    prompt = build_prompt(
        "gem1",
        {
            "search_id": "SEARCH-TEST-001",
            "candidate_id": "CAND-001",
            "cv_text": "Sample CV",
            "interview_notes": "Sample Notes",
            "gem5_summary": "Sample GEM5 summary",
        },
    )
    assert isinstance(prompt, str)
    assert "SEARCH-TEST-001" in prompt
    assert "CAND-001" in prompt
    assert "{{search_id}}" not in prompt
    assert "{{candidate_id}}" not in prompt


def test_get_required_variables():
    vars_gem1 = get_required_variables("gem1")
    assert "search_id" in vars_gem1
    assert "candidate_id" in vars_gem1
    assert "PROMPT_MAESTRO" not in vars_gem1
    assert "VERSION" not in vars_gem1
