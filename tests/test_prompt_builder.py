import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt():
    prompt = load_prompt("gem5")
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_prompt_builder_cache_and_invalidation(tmp_path, monkeypatch):
    test_prompts_dir = str(tmp_path)
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", test_prompts_dir)

    prompt_file = tmp_path / "test_gem.md"
    prompt_file.write_text("Hello {{name}}", encoding="utf-8")

    _load_prompt_cached.cache_clear()

    # First load - cache miss
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}"

    info1 = _load_prompt_cached.cache_info()
    assert info1.misses >= 1

    # Second load - cache hit
    content2 = load_prompt("test_gem")
    assert content2 == "Hello {{name}}"

    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == info1.hits + 1

    # Modify file mtime using utime to simulate file edit
    prompt_file.write_text("Hello updated {{name}}", encoding="utf-8")
    new_time = time.time() + 10
    os.utime(str(prompt_file), (new_time, new_time))

    content3 = load_prompt("test_gem")
    assert content3 == "Hello updated {{name}}"


def test_build_prompt(tmp_path, monkeypatch):
    test_prompts_dir = str(tmp_path)
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", test_prompts_dir)

    maestro_file = tmp_path / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO_RULES", encoding="utf-8")

    gem_file = tmp_path / "test_agent.md"
    gem_file.write_text("Header\n{{PROMPT_MAESTRO}}\nInput: {{input}}", encoding="utf-8")

    _load_prompt_cached.cache_clear()

    built = build_prompt("test_agent", {"input": "Senior Engineer"})
    assert "MAESTRO_RULES" in built
    assert "Input: Senior Engineer" in built
    assert "{{PROMPT_MAESTRO}}" not in built


def test_get_required_variables():
    vars_list = get_required_variables("gem5")
    assert "PROMPT_MAESTRO" not in vars_list
    assert "VERSION" not in vars_list
