import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_caching_and_invalidation(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    test_prompt_file = prompts_dir / "test_gem.md"
    test_prompt_file.write_text("Hello {{name}}!", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    # Initial load - should be cache miss
    info_before = _load_prompt_cached.cache_info()
    content1 = load_prompt("test_gem")
    info_after1 = _load_prompt_cached.cache_info()

    assert content1 == "Hello {{name}}!"
    assert info_after1.hits == info_before.hits
    assert info_after1.misses == info_before.misses + 1

    # Second load without modifying file - should be cache hit
    content2 = load_prompt("test_gem")
    info_after2 = _load_prompt_cached.cache_info()

    assert content2 == "Hello {{name}}!"
    assert info_after2.hits == info_after1.hits + 1

    # Modify file and update mtime
    time.sleep(0.01)
    new_mtime = time.time() + 10.0
    test_prompt_file.write_text("Updated {{name}}!", encoding="utf-8")
    os.utime(str(test_prompt_file), (new_mtime, new_mtime))

    content3 = load_prompt("test_gem")
    info_after3 = _load_prompt_cached.cache_info()

    assert content3 == "Updated {{name}}!"
    assert info_after3.misses == info_after2.misses + 1


def test_build_prompt_and_variables(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO_HEADER\n", encoding="utf-8")

    gem_file = prompts_dir / "gem_demo.md"
    gem_file.write_text(
        "{{PROMPT_MAESTRO}}\nRole: {{role}}, Task: {{task}}", encoding="utf-8"
    )

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    req_vars = get_required_variables("gem_demo")
    assert set(req_vars) == {"role", "task"}

    built = build_prompt("gem_demo", {"role": "Engineer", "task": "Optimize"})
    assert "MAESTRO_HEADER" in built
    assert "Role: Engineer, Task: Optimize" in built
