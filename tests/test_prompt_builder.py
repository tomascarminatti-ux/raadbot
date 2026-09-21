import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_caching_and_invalidation(tmp_path, monkeypatch):
    # Set up temp prompt directory
    test_gem = "test_gem_sample"
    prompt_file = tmp_path / f"{test_gem}.md"
    prompt_file.write_text("Hello {{name}}, welcome to {{service}}!")

    # Patch PROMPTS_DIR in prompt_builder
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))

    # Clear LRU cache before test
    _load_prompt_cached.cache_clear()

    # Initial load (Cache Miss)
    content1 = load_prompt(test_gem)
    assert content1 == "Hello {{name}}, welcome to {{service}}!"
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Second load without modifying file (Cache Hit)
    content2 = load_prompt(test_gem)
    assert content2 == content1
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1
    assert info2.misses == 1

    # Modify file and update mtime
    new_text = "Updated template for {{name}} in {{service}}!"
    prompt_file.write_text(new_text)

    # Force mtime update using os.utime to ensure mtime changes across filesystems
    stat = os.stat(str(prompt_file))
    os.utime(str(prompt_file), (stat.st_atime, stat.st_mtime + 2.0))

    # Load after mtime change (Cache Miss due to new mtime key)
    content3 = load_prompt(test_gem)
    assert content3 == new_text
    info3 = _load_prompt_cached.cache_info()
    assert info3.misses == 2


def test_build_prompt(tmp_path, monkeypatch):
    maestro_file = tmp_path / "00_prompt_maestro.md"
    maestro_file.write_text("[MAESTRO HEADER]")

    gem_file = tmp_path / "gem_test.md"
    gem_file.write_text("System: {{PROMPT_MAESTRO}}\nTask for {{candidate}}.")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))
    _load_prompt_cached.cache_clear()

    result = build_prompt("gem_test", {"candidate": "John Doe"})
    assert "[MAESTRO HEADER]" in result
    assert "Task for John Doe." in result


def test_get_required_variables(tmp_path, monkeypatch):
    gem_file = tmp_path / "gem_vars.md"
    gem_file.write_text("Context: {{PROMPT_MAESTRO}}, {{VERSION}}, Target: {{role}} in {{location}}.")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))
    _load_prompt_cached.cache_clear()

    required = get_required_variables("gem_vars")
    assert set(required) == {"role", "location"}
