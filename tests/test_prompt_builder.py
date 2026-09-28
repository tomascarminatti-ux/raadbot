import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    _load_prompt_cached,
)


def test_prompt_builder_caching_and_invalidation(tmp_path, monkeypatch):
    # Set up temporary prompts directory
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    monkeypatch.setattr("agent.prompt_builder.PROMPTS_DIR", str(prompts_dir))

    # Create dummy prompt
    prompt_file = prompts_dir / "gem_test.md"
    prompt_file.write_text("Hello {{name}}!", encoding="utf-8")

    # Clear cache before test
    _load_prompt_cached.cache_clear()

    # First load -> cache miss
    content1 = load_prompt("gem_test")
    assert content1 == "Hello {{name}}!"
    info1 = _load_prompt_cached.cache_info()

    # Second load -> cache hit
    content2 = load_prompt("gem_test")
    assert content2 == "Hello {{name}}!"
    info2 = _load_prompt_cached.cache_info()
    assert info2.hits > info1.hits

    # Update file mtime using os.utime to simulate file edit
    new_mtime = os.path.getmtime(str(prompt_file)) + 10
    os.utime(str(prompt_file), (new_mtime, new_mtime))

    # Third load -> cache miss due to mtime change
    prompt_file.write_text("Updated {{name}}!", encoding="utf-8")
    os.utime(str(prompt_file), (new_mtime, new_mtime))
    content3 = load_prompt("gem_test")
    assert content3 == "Updated {{name}}!"


def test_build_prompt_placeholders():
    prompt = build_prompt("gem1", {"input": "test_input"})
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_get_required_variables():
    vars_list = get_required_variables("gem1")
    assert isinstance(vars_list, list)


def test_prompt_loading_benchmark():
    _load_prompt_cached.cache_clear()
    t0 = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", {"input": "test"})
    t1 = time.perf_counter()
    elapsed = t1 - t0
    ms_per_call = (elapsed / iterations) * 1000
    print(
        f"\n⚡ Benchmark: {iterations} iterations in {elapsed:.4f}s "
        f"({ms_per_call:.4f} ms/call)"
    )
    assert ms_per_call < 0.05  # Cached loading should be under 0.05ms
