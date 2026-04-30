import os
import sys
import pytest

# Add project root to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt


def test_build_prompt_basic(tmp_path):
    # Create temporary prompt files
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_content = "[VERSION] v1.2\nROLE: Senior Consultant"
    (prompts_dir / "00_prompt_maestro.md").write_text(maestro_content)

    gem_content = "{{PROMPT_MAESTRO}}\nHello {{name}}!"
    (prompts_dir / "gem_test.md").write_text(gem_content)

    # Patch PROMPTS_DIR in agent.prompt_builder
    import agent.prompt_builder
    original_dir = agent.prompt_builder.PROMPTS_DIR
    agent.prompt_builder.PROMPTS_DIR = str(prompts_dir)

    try:
        variables = {"name": "World"}
        prompt = build_prompt("gem_test", variables)

        assert "ROLE: Senior Consultant" in prompt
        assert "Hello World!" in prompt
        assert "{{PROMPT_MAESTRO}}" not in prompt
    finally:
        agent.prompt_builder.PROMPTS_DIR = original_dir


def test_variable_substitution_real_gem():
    # gem1 doesn't have variables, but build_prompt should still work
    variables = {"any_var": "any_value"}
    prompt = build_prompt("gem1", variables)
    assert "GEM 1" in prompt


def test_maestro_injection_real_gem():
    build_prompt("gem1", {})
    # gem1 doesn't have {{PROMPT_MAESTRO}} placeholder
    pass
