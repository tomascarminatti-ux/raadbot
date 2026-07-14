import os
import sys
import pytest

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt, clear_prompt_caches, load_prompt

def test_build_prompt_basic(tmp_path, monkeypatch):
    # Setup temporary prompts directory
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO: {{version}}")

    gem_file = prompts_dir / "test_gem.md"
    gem_file.write_text("GEM: {{PROMPT_MAESTRO}} - DATA: {{data}}")

    # Patch PROMPTS_DIR in prompt_builder
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))

    # Clear caches to ensure we use our temp files
    clear_prompt_caches()

    variables = {"version": "1.0", "data": "hello"}
    result = build_prompt("test_gem", variables)

    assert result == "GEM: MAESTRO: 1.0 - DATA: hello"

def test_build_prompt_caching(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("V1")

    gem_file = prompts_dir / "test_gem.md"
    gem_file.write_text("{{PROMPT_MAESTRO}}")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    clear_prompt_caches()

    # First load
    assert build_prompt("test_gem", {}) == "V1"

    # Modify file on disk
    maestro_file.write_text("V2")

    # Should still return V1 due to cache
    assert build_prompt("test_gem", {}) == "V1"

    # Clear cache
    clear_prompt_caches()

    # Should now return V2
    assert build_prompt("test_gem", {}) == "V2"

def test_build_prompt_missing_variable(tmp_path, monkeypatch, capsys):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("M")

    gem_file = prompts_dir / "test_gem.md"
    gem_file.write_text("{{PROMPT_MAESTRO}} {{missing}}")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    clear_prompt_caches()

    result = build_prompt("test_gem", {})
    assert "{{missing}}" in result

    captured = capsys.readouterr()
    assert "Variables sin reemplazar: ['missing']" in captured.out
