import pytest
import os
from agent.prompt_builder import build_prompt, load_prompt, load_maestro, get_required_variables, clear_prompt_caches

def test_build_prompt_correctness():
    # Clear caches to ensure we start clean
    clear_prompt_caches()

    # Build prompt for gem1
    variables = {
        "ROL": "test-role-value",
    }
    prompt = build_prompt("gem1", variables)

    # Assert maestro is injected
    assert "00_prompt_maestro" not in prompt # Prompt name should not be there literally, but maestro content should
    assert "RAAD" in prompt

    # Assert variables are injected (even if none was in template, check that it doesn't crash)
    assert len(prompt) > 0

def test_missing_prompt_raises_error():
    with pytest.raises(FileNotFoundError):
        build_prompt("non_existent_gem_xyz", {})

def test_clear_caches():
    clear_prompt_caches()
    # Loading after clearing should still work perfectly
    maestro = load_maestro()
    assert len(maestro) > 0
