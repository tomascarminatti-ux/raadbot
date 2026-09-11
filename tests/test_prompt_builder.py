import os
import time
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    clear_prompt_caches,
    _load_prompt_cached,
    PROMPTS_DIR,
)


def test_load_prompt_and_caching():
    clear_prompt_caches()
    cache_info_initial = _load_prompt_cached.cache_info()
    assert cache_info_initial.hits == 0

    content1 = load_prompt("gem1")
    assert "gem1" in content1.lower() or len(content1) > 0

    # Second load should hit cache
    content2 = load_prompt("gem1")
    assert content1 == content2
    cache_info_after = _load_prompt_cached.cache_info()
    assert cache_info_after.hits >= 1


def test_mtime_invalidation():
    clear_prompt_caches()
    temp_path = os.path.join(PROMPTS_DIR, "temp_test_prompt.md")

    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write("Initial content {{var1}}")

        first_read = load_prompt("temp_test_prompt")
        assert "Initial content" in first_read

        # Simulate update by updating content and mtime via os.utime
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write("Updated content {{var1}}")

        new_mtime = time.time() + 10.0
        os.utime(temp_path, (new_mtime, new_mtime))

        second_read = load_prompt("temp_test_prompt")
        assert "Updated content" in second_read

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        clear_prompt_caches()


def test_clear_prompt_caches():
    load_prompt("gem1")
    assert _load_prompt_cached.cache_info().currsize > 0

    clear_prompt_caches()
    assert _load_prompt_cached.cache_info().currsize == 0


def test_build_prompt():
    clear_prompt_caches()
    prompt = build_prompt("gem1", {
        "search_id": "TEST-123",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV text",
        "interview_notes": "Sample notes",
        "gem5_summary": "Sample summary",
    })
    assert "TEST-123" in prompt
    assert "CAND-001" in prompt
    assert "Sample CV text" in prompt


def test_get_required_variables():
    vars_list = get_required_variables("gem1")
    assert "search_id" in vars_list or "candidate_id" in vars_list
