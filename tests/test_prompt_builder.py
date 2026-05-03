
import os
import pytest
from agent.prompt_builder import build_prompt, load_prompt, get_required_variables

def test_build_prompt_basic():
    variables = {
        "search_id": "S1",
        "candidate_id": "C1",
        "cv_text": "CV content",
        "interview_notes": "Notes content",
        "gem5_summary": "Summary content"
    }
    prompt = build_prompt("gem1", variables)

    assert "S1" in prompt
    assert "C1" in prompt
    assert "CV content" in prompt
    # Maestro content should be there
    assert "RAAD" in prompt
    assert "[ROLE]" in prompt

def test_build_prompt_with_dict():
    variables = {
        "search_id": "S1",
        "candidate_id": "C1",
        "cv_text": "CV content",
        "interview_notes": "Notes content",
        "gem5_summary": {"key": "value"}
    }
    prompt = build_prompt("gem1", variables)
    assert '"key": "value"' in prompt

def test_get_required_variables():
    vars = get_required_variables("gem1")
    assert "search_id" in vars
    assert "candidate_id" in vars
    assert "PROMPT_MAESTRO" not in vars
    assert "VERSION" not in vars
