import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_caching(tmp_path, monkeypatch):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()
    prompt_file = prompt_dir / "test_gem.md"
    prompt_file.write_text("Hello {{name}}! Welcome to {{PROMPT_MAESTRO}}.", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompt_dir))

    # Clear cache before test
    _load_prompt_cached.cache_clear()
    info_before = _load_prompt_cached.cache_info()

    # First load -> Cache Miss
    content1 = load_prompt("test_gem")
    assert content1 == "Hello {{name}}! Welcome to {{PROMPT_MAESTRO}}."
    info_after1 = _load_prompt_cached.cache_info()
    assert info_after1.misses == info_before.misses + 1

    # Second load -> Cache Hit
    content2 = load_prompt("test_gem")
    assert content2 == content1
    info_after2 = _load_prompt_cached.cache_info()
    assert info_after2.hits == info_after1.hits + 1

    # Modify file and update mtime -> Cache Miss on new mtime
    new_time = time.time() + 10.0
    prompt_file.write_text("Updated {{name}}! Welcome to {{PROMPT_MAESTRO}}.", encoding="utf-8")
    os.utime(str(prompt_file), (new_time, new_time))

    content3 = load_prompt("test_gem")
    assert content3 == "Updated {{name}}! Welcome to {{PROMPT_MAESTRO}}."
    info_after3 = _load_prompt_cached.cache_info()
    assert info_after3.misses == info_after2.misses + 1


def test_build_prompt_and_variables(tmp_path, monkeypatch):
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()

    maestro_file = prompt_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO INSTRUCTIONS", encoding="utf-8")

    gem_file = prompt_dir / "gem_test.md"
    gem_file.write_text("Role: {{role}}. {{PROMPT_MAESTRO}} Data: {{data}}", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompt_dir))

    _load_prompt_cached.cache_clear()

    # Test required variables extraction
    req_vars = get_required_variables("gem_test")
    assert set(req_vars) == {"role", "data"}

    # Test prompt building with variables
    result = build_prompt("gem_test", {"role": "Engineer", "data": {"key": "val"}})
    assert "Role: Engineer." in result
    assert "MAESTRO INSTRUCTIONS" in result
    assert '"key": "val"' in result
