import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_prompt_builder_caching_and_invalidation(tmp_path, monkeypatch):
    # Setup temporary prompts directory
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO PROMPT CONTENT", encoding="utf-8")

    gem_file = prompts_dir / "test_gem.md"
    gem_file.write_text(
        "{{PROMPT_MAESTRO}}\nHello {{candidate_name}}, welcome to {{company}}!",
        encoding="utf-8"
    )

    import agent.prompt_builder as pb
    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))
    pb._load_prompt_cached.cache_clear()

    # Initial load (Cache Miss)
    initial_info = pb._load_prompt_cached.cache_info()
    prompt_text = load_prompt("test_gem")
    assert "Hello {{candidate_name}}" in prompt_text
    curr_info = pb._load_prompt_cached.cache_info()
    assert curr_info.hits == initial_info.hits
    assert curr_info.misses == initial_info.misses + 1

    # Second load (Cache Hit)
    prompt_text_2 = load_prompt("test_gem")
    assert prompt_text_2 == prompt_text
    hit_info = pb._load_prompt_cached.cache_info()
    assert hit_info.hits == curr_info.hits + 1

    # Update file mtime (Cache Invalidation)
    new_content = "{{PROMPT_MAESTRO}}\nUpdated greeting for {{candidate_name}}!"
    gem_file.write_text(new_content, encoding="utf-8")
    future_time = time.time() + 10
    os.utime(str(gem_file), (future_time, future_time))

    updated_text = load_prompt("test_gem")
    assert "Updated greeting for" in updated_text
    invalidation_info = pb._load_prompt_cached.cache_info()
    assert invalidation_info.misses == hit_info.misses + 1


def test_build_prompt_and_required_variables(tmp_path, monkeypatch):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()

    maestro_file = prompts_dir / "00_prompt_maestro.md"
    maestro_file.write_text("MAESTRO RULE", encoding="utf-8")

    gem_file = prompts_dir / "gem_test.md"
    gem_file.write_text(
        "{{PROMPT_MAESTRO}}\nCandidate: {{candidate_name}}, Role: {{role}}",
        encoding="utf-8"
    )

    import agent.prompt_builder as pb
    monkeypatch.setattr(pb, "PROMPTS_DIR", str(prompts_dir))

    req_vars = get_required_variables("gem_test")
    assert set(req_vars) == {"candidate_name", "role"}

    built = build_prompt("gem_test", {"candidate_name": "Alice", "role": "Engineer"})
    assert "MAESTRO RULE" in built
    assert "Candidate: Alice, Role: Engineer" in built
