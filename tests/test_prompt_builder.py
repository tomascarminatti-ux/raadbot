import pytest
from agent.prompt_builder import build_prompt, clear_prompt_caches, get_required_variables

def test_build_prompt_basic():
    # Clear cache first
    clear_prompt_caches()

    # Let's test using a prompt like gem1
    variables = {
        "search_id": "SRCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV",
        "interview_notes": "Sample Notes",
        "gem5_summary": "Sample Summary",
    }

    prompt = build_prompt("gem1", variables)

    # Assert variables are in the final prompt
    assert "SRCH-001" in prompt
    assert "CAND-001" in prompt
    assert "Sample CV" in prompt
    assert "Sample Notes" in prompt
    assert "Sample Summary" in prompt
    # Check that prompt maestro context is included
    assert "PROMPT_MAESTRO" not in prompt


def test_build_prompt_with_dict():
    variables = {
        "search_id": "SRCH-002",
        "candidate_id": "CAND-002",
        "cv_text": {"key": "val"},
        "interview_notes": "Sample Notes",
        "gem5_summary": "Sample Summary",
    }

    prompt = build_prompt("gem1", variables)
    assert "SRCH-002" in prompt
    assert "val" in prompt


def test_get_required_variables():
    req = get_required_variables("gem1")
    assert "search_id" in req
    assert "candidate_id" in req
    assert "cv_text" in req
    assert "interview_notes" in req
    assert "gem5_summary" in req
    assert "PROMPT_MAESTRO" not in req
    assert "VERSION" not in req
