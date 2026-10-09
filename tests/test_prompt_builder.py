import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_load_prompt_and_caching(tmp_path, monkeypatch):
    # Setup temporary prompts directory
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    test_file = prompts_dir / "gem_test.md"
    test_file.write_text("Hello {{name}}!", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))

    # Clear cache before test
    _load_prompt_cached.cache_clear()

    # Initial load
    content1 = load_prompt("gem_test")
    assert content1 == "Hello {{name}}!"

    hits_before = _load_prompt_cached.cache_info().hits

    # Second load (should hit cache)
    content2 = load_prompt("gem_test")
    assert content2 == "Hello {{name}}!"
    assert _load_prompt_cached.cache_info().hits == hits_before + 1

    # Modify file mtime/content
    time.sleep(0.01)
    test_file.write_text("Updated {{name}}!", encoding="utf-8")

    # Third load (should fetch updated content due to mtime change)
    content3 = load_prompt("gem_test")
    assert content3 == "Updated {{name}}!"


def test_build_prompt(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO_RULES", encoding="utf-8")

    gem_file = prompts_dir / "gem_demo.md"
    gem_file.write_text(
        "System: {{PROMPT_MAESTRO}}\nUser: {{user_val}}", encoding="utf-8"
    )

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    result = build_prompt("gem_demo", {"user_val": "world"})
    assert result == "System: MAESTRO_RULES\nUser: world"


def test_get_required_variables(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    gem_file = prompts_dir / "gem_vars.md"
    gem_file.write_text(
        "{{PROMPT_MAESTRO}} {{VERSION}} {{var1}} {{var2}}", encoding="utf-8"
    )

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))
    _load_prompt_cached.cache_clear()

    req_vars = get_required_variables("gem_vars")
    assert sorted(req_vars) == ["var1", "var2"]
