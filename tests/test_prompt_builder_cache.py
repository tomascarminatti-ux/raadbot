import os
import time
from agent.prompt_builder import load_prompt, _load_prompt_cached


def test_load_prompt_caching(tmp_path):
    # Setup temporary prompt file in a temp directory
    test_gem_dir = tmp_path / "prompts"
    test_gem_dir.mkdir()

    # Monkeypatch the PROMPTS_DIR
    import agent.prompt_builder as pb
    original_prompts_dir = pb.PROMPTS_DIR
    pb.PROMPTS_DIR = str(test_gem_dir)

    try:
        gem_name = "test_gem"
        file_path = test_gem_dir / f"{gem_name}.md"

        # 1. Write initial content
        file_path.write_text("Hello World", encoding="utf-8")

        # Clear cache before running test
        _load_prompt_cached.cache_clear()

        # Load for the first time
        content1 = load_prompt(gem_name)
        assert content1 == "Hello World"

        # Verify hit count or check that same content is returned
        info_before = _load_prompt_cached.cache_info()
        assert info_before.hits == 0
        assert info_before.misses == 1

        # 2. Load again (should hit cache)
        content2 = load_prompt(gem_name)
        assert content2 == "Hello World"

        info_after = _load_prompt_cached.cache_info()
        assert info_after.hits == 1
        assert info_after.misses == 1

        # 3. Modify file on disk and force mtime change explicitly using os.utime
        # to avoid filesystem mtime resolution limits causing test flakiness
        file_path.write_text("Hello Modified World", encoding="utf-8")
        current_mtime = os.path.getmtime(file_path)
        os.utime(file_path, (current_mtime + 2.0, current_mtime + 2.0))

        # Load again (should invalidate cache and reload)
        content3 = load_prompt(gem_name)
        assert content3 == "Hello Modified World"

        info_final = _load_prompt_cached.cache_info()
        assert info_final.misses == 2

    finally:
        # Restore PROMPTS_DIR
        pb.PROMPTS_DIR = original_prompts_dir
