import os
import time
import pytest
import agent.prompt_builder as pb
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching():
    # Test loading real prompt
    prompt = load_prompt("gem5")
    assert isinstance(prompt, str)
    assert len(prompt) > 0

    # Verify cache hit on second load
    initial_hits = _load_prompt_cached.cache_info().hits
    prompt_again = load_prompt("gem5")
    assert prompt == prompt_again
    assert _load_prompt_cached.cache_info().hits > initial_hits


def test_prompt_cache_invalidation(tmp_path):
    temp_dir = tmp_path / "prompts"
    temp_dir.mkdir()
    prompt_file = temp_dir / "temp_gem.md"

    # Write initial version
    prompt_file.write_text("Hello {{name}} v1", encoding="utf-8")

    # Monkeypatch PROMPTS_DIR
    original_dir = pb.PROMPTS_DIR
    pb.PROMPTS_DIR = str(temp_dir)

    try:
        content1 = pb.load_prompt("temp_gem")
        assert content1 == "Hello {{name}} v1"

        # Update file content and advance mtime
        new_time = time.time() + 10
        prompt_file.write_text("Hello {{name}} v2", encoding="utf-8")
        os.utime(str(prompt_file), (new_time, new_time))

        content2 = pb.load_prompt("temp_gem")
        assert content2 == "Hello {{name}} v2"
    finally:
        pb.PROMPTS_DIR = original_dir


def test_build_prompt_and_variables(tmp_path):
    temp_dir = tmp_path / "prompts"
    temp_dir.mkdir()

    # Create maestro and gem prompt in temp_dir
    (temp_dir / "00_prompt_maestro.md").write_text("MAESTRO PROMPT", encoding="utf-8")
    (temp_dir / "test_gem.md").write_text("Base {{PROMPT_MAESTRO}} - Input: {{candidate_info}} - {{VERSION}}", encoding="utf-8")

    original_dir = pb.PROMPTS_DIR
    pb.PROMPTS_DIR = str(temp_dir)

    try:
        built = pb.build_prompt("test_gem", {"candidate_info": "Jane Doe, Senior Dev"})
        assert "MAESTRO PROMPT" in built
        assert "Jane Doe, Senior Dev" in built
        assert "{{candidate_info}}" not in built

        required = pb.get_required_variables("test_gem")
        assert required == ["candidate_info"]
    finally:
        pb.PROMPTS_DIR = original_dir
