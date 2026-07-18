import pytest
import re
from agent.prompt_builder import build_prompt, clear_prompt_caches, load_prompt, load_maestro

def test_prompt_builder_correctness():
    # Make sure cache is cleared
    clear_prompt_caches()

    variables = {
        "search_id": "SEARCH-2026-TEST",
        "candidate_id": "CAND-TEST",
        "cv_text": "Experienced Director of Operations.",
        "interview_notes": "Very structured, good communication.",
        "gem5_summary": "Summary context details.",
    }

    prompt = build_prompt("gem1", variables)

    # Check that maestro content was injected
    assert "PROMPT_MAESTRO" not in prompt
    assert "RAAD" in prompt or "Industrial" in prompt or "GEM" in prompt

    # Check that variables were correctly substituted
    assert "SEARCH-2026-TEST" in prompt
    assert "CAND-TEST" in prompt
    assert "Experienced Director of Operations." in prompt
    assert "Very structured, good communication." in prompt
    assert "Summary context details." in prompt

    # Check that unmatched variables (like VERSION) are untouched and do not cause error
    assert "VERSION" in prompt or "{{VERSION}}" in prompt
