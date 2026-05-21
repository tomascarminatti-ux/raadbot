import pytest
import os
import json
from agent.prompt_builder import build_prompt, get_required_variables, load_prompt, load_maestro

def test_load_prompt():
    content = load_prompt("gem1")
    assert "{{PROMPT_MAESTRO}}" in content
    assert "{{cv_text}}" in content

def test_load_maestro():
    content = load_maestro()
    assert "RAAD" in content

def test_build_prompt_basic():
    variables = {
        "search_id": "S1",
        "candidate_id": "C1",
        "cv_text": "CV content",
        "interview_notes": "Notes",
        "gem5_summary": "Summary"
    }
    prompt = build_prompt("gem1", variables)

    assert "S1" in prompt
    assert "C1" in prompt
    assert "CV content" in prompt
    assert "{{cv_text}}" not in prompt
    assert "{{PROMPT_MAESTRO}}" not in prompt

def test_build_prompt_with_dict():
    variables = {
        "search_id": "S1",
        "candidate_id": "C1",
        "cv_text": "CV",
        "interview_notes": "Notes",
        "gem5_summary": {"key": "value"}
    }
    prompt = build_prompt("gem1", variables)
    assert '"key": "value"' in prompt

def test_build_prompt_missing_vars():
    variables = {"search_id": "S1"}
    prompt = build_prompt("gem1", variables)
    assert "{{cv_text}}" in prompt

def test_get_required_variables():
    vars = get_required_variables("gem1")
    assert "cv_text" in vars
    assert "search_id" in vars
    assert "PROMPT_MAESTRO" not in vars
    assert "VERSION" not in vars

def test_caching():
    p1 = load_prompt("gem1")
    p2 = load_prompt("gem1")
    assert p1 is p2
