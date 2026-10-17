from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    _load_prompt_cached,
    get_required_variables,
)


def test_prompt_builder_caching(tmp_path, monkeypatch):
    # Set up temporary prompt directory
    prompt_file = tmp_path / "test_gem.md"
    prompt_file.write_text("Hello {{name}}! {{PROMPT_MAESTRO}}", encoding="utf-8")

    maestro_file = tmp_path / "00_prompt_maestro.md"
    maestro_file.write_text("Maestro content", encoding="utf-8")

    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(tmp_path))

    _load_prompt_cached.cache_clear()

    # Initial load
    p1 = load_prompt("test_gem")
    assert "Hello {{name}}!" in p1
    info1 = _load_prompt_cached.cache_info()
    assert info1.hits == 0

    # Second load should hit cache
    p2 = load_prompt("test_gem")
    assert p2 == p1
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits == 1

    # Build prompt test
    built = build_prompt("test_gem", {"name": "World"})
    assert "Hello World! Maestro content" in built

    # Required variables
    req = get_required_variables("test_gem")
    assert req == ["name"]
