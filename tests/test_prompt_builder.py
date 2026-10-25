import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached
)

def test_load_prompt_caching(tmp_path, monkeypatch):
    # Set up temp prompt dir
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))

    # Clear LRU cache before test
    _load_prompt_cached.cache_clear()

    # Create dummy prompt
    dummy_file = prompts_dir / "gem_test.md"
    dummy_file.write_text("Hello {{name}}!", encoding="utf-8")

    # Initial load (cache miss)
    info_before = _load_prompt_cached.cache_info()
    content1 = load_prompt("gem_test")
    assert content1 == "Hello {{name}}!"
    info_after1 = _load_prompt_cached.cache_info()
    assert info_after1.misses == info_before.misses + 1

    # Second load (cache hit)
    content2 = load_prompt("gem_test")
    assert content2 == "Hello {{name}}!"
    info_after2 = _load_prompt_cached.cache_info()
    assert info_after2.hits == info_after1.hits + 1

    # Update file modification time and content (cache invalidation)
    time.sleep(0.01)
    dummy_file.write_text("Updated {{name}}!", encoding="utf-8")
    new_mtime = os.path.getmtime(str(dummy_file)) + 1.0
    os.utime(str(dummy_file), (new_mtime, new_mtime))

    content3 = load_prompt("gem_test")
    assert content3 == "Updated {{name}}!"
    info_after3 = _load_prompt_cached.cache_info()
    assert info_after3.misses == info_after2.misses + 1


def test_build_prompt_placeholders(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO RULE", encoding="utf-8")

    gem_file = prompts_dir / "gem1.md"
    gem_file.write_text("{{PROMPT_MAESTRO}}\nCandidate: {{candidate_id}}", encoding="utf-8")

    result = build_prompt("gem1", {"candidate_id": "CAND-123"})
    assert "MAESTRO RULE" in result
    assert "Candidate: CAND-123" in result


def test_get_required_variables(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    gem_file = prompts_dir / "gem2.md"
    gem_file.write_text("Input: {{input_var}} and {{other_var}}, auto: {{PROMPT_MAESTRO}}, ver: {{VERSION}}", encoding="utf-8")

    req_vars = get_required_variables("gem2")
    assert set(req_vars) == {"input_var", "other_var"}
