import os
import time
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    clear_prompt_caches,
    _load_prompt_cached,
    PROMPTS_DIR,
)


def test_prompt_builder_cache_and_invalidation(tmp_path):
    clear_prompt_caches()

    # Create temporary prompt in real prompts directory to test load_prompt
    test_prompt_path = os.path.join(PROMPTS_DIR, "temp_test_prompt.md")
    with open(test_prompt_path, "w", encoding="utf-8") as f:
        f.write("Initial content {{foo}}")

    try:
        # First call: cache miss
        cache_info_before = _load_prompt_cached.cache_info()
        content1 = load_prompt("temp_test_prompt")
        assert content1 == "Initial content {{foo}}"
        cache_info_after1 = _load_prompt_cached.cache_info()
        assert cache_info_after1.hits == cache_info_before.hits
        assert cache_info_after1.misses == cache_info_before.misses + 1

        # Second call: cache hit
        content2 = load_prompt("temp_test_prompt")
        assert content2 == "Initial content {{foo}}"
        cache_info_after2 = _load_prompt_cached.cache_info()
        assert cache_info_after2.hits == cache_info_after1.hits + 1

        # Update file mtime using os.utime to test cache invalidation
        time.sleep(0.01)
        with open(test_prompt_path, "w", encoding="utf-8") as f:
            f.write("Updated content {{foo}}")
        now = time.time() + 1.0
        os.utime(test_prompt_path, (now, now))

        # Third call: new mtime causes cache miss and returns updated content
        content3 = load_prompt("temp_test_prompt")
        assert content3 == "Updated content {{foo}}"
        cache_info_after3 = _load_prompt_cached.cache_info()
        assert cache_info_after3.misses == cache_info_after2.misses + 1

    finally:
        if os.path.exists(test_prompt_path):
            os.remove(test_prompt_path)
        clear_prompt_caches()


def test_clear_prompt_caches():
    clear_prompt_caches()
    load_prompt("gem6")
    cache_info = _load_prompt_cached.cache_info()
    assert cache_info.currsize > 0

    clear_prompt_caches()
    cache_info_after = _load_prompt_cached.cache_info()
    assert cache_info_after.currsize == 0


def test_build_prompt():
    clear_prompt_caches()
    test_prompt_path = os.path.join(PROMPTS_DIR, "temp_test_build.md")
    with open(test_prompt_path, "w", encoding="utf-8") as f:
        f.write("Hello {{PROMPT_MAESTRO}} - Search: {{search_id}} Candidate: {{candidate_id}}")

    try:
        prompt = build_prompt(
            "temp_test_build",
            {"search_id": "TEST_SEARCH", "candidate_id": "TEST_CANDIDATE"}
        )
        assert "TEST_SEARCH" in prompt
        assert "TEST_CANDIDATE" in prompt
    finally:
        if os.path.exists(test_prompt_path):
            os.remove(test_prompt_path)
        clear_prompt_caches()


def test_get_required_variables():
    clear_prompt_caches()
    test_prompt_path = os.path.join(PROMPTS_DIR, "temp_test_vars.md")
    with open(test_prompt_path, "w", encoding="utf-8") as f:
        f.write("Hello {{PROMPT_MAESTRO}} - {{my_var_1}} and {{my_var_2}}")

    try:
        vars_list = get_required_variables("temp_test_vars")
        assert "my_var_1" in vars_list
        assert "my_var_2" in vars_list
        assert "PROMPT_MAESTRO" not in vars_list
    finally:
        if os.path.exists(test_prompt_path):
            os.remove(test_prompt_path)
        clear_prompt_caches()
