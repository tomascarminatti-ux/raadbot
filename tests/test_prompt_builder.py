import pytest
import os
import re
from agent.prompt_builder import (
    load_prompt,
    load_maestro,
    build_prompt,
    build_agent_prompt,
    get_required_variables,
    clear_prompt_caches
)

def test_load_prompt_and_maestro():
    # Test loading of existing prompts
    maestro = load_maestro()
    assert isinstance(maestro, str)
    assert len(maestro) > 0

    gem5_prompt = load_prompt("gem5")
    assert isinstance(gem5_prompt, str)
    assert len(gem5_prompt) > 0

    # Test loading non-existent prompt raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_prompt("non_existent_gem_xyz")

def test_build_agent_prompt_variables_injection():
    # Test variable injection via agent helper
    variables = {
        "input": "test_input_value_123",
        "custom_var": "custom_val_456"
    }
    prompt = build_agent_prompt("gem5", variables)
    assert "test_input_value_123" in prompt
    assert "custom_val_456" in prompt

def test_get_required_variables():
    required = get_required_variables("gem5")
    assert isinstance(required, list)
    # Since gem5.md has no explicit {{ }} placeholders, it should be empty
    assert required == []

def test_clear_prompt_caches():
    # Invalidate cache
    clear_prompt_caches()
    # Cache should be cleared and load_prompt should still work
    gem5_prompt = load_prompt("gem5")
    assert isinstance(gem5_prompt, str)
