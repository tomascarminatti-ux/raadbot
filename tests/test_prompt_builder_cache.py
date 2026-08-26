import os
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_caches, build_prompt, PROMPTS_DIR

def test_load_prompt_lru_cache():
    clear_prompt_caches()
    # Initial load
    content1 = load_prompt("gem1")
    info1 = load_prompt.cache_info()
    assert info1.hits == 0
    assert info1.misses == 1

    # Second load should hit cache
    content2 = load_prompt("gem1")
    info2 = load_prompt.cache_info()
    assert content1 == content2
    assert info2.hits == 1
    assert info2.misses == 1

def test_clear_prompt_caches():
    clear_prompt_caches()
    load_prompt("gem1")
    assert load_prompt.cache_info().hits == 0

    clear_prompt_caches()
    info = load_prompt.cache_info()
    assert info.hits == 0
    assert info.misses == 0

    # Next call counts as a miss again
    load_prompt("gem1")
    assert load_prompt.cache_info().misses == 1

def test_build_prompt_with_cached_templates():
    clear_prompt_caches()

    # Create temporary prompt template with variables for testing
    temp_gem = "_test_temp_gem"
    temp_filepath = os.path.join(PROMPTS_DIR, f"{temp_gem}.md")
    try:
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("{{PROMPT_MAESTRO}}\nHello {{candidate_name}}, welcome to {{company_name}}.")

        prompt = build_prompt(temp_gem, {"candidate_name": "Alice", "company_name": "Acme Corp"})
        assert "Alice" in prompt
        assert "Acme Corp" in prompt
        assert "[ROLE]" in prompt  # Injected from PROMPT_MAESTRO
        assert "{{PROMPT_MAESTRO}}" not in prompt
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        clear_prompt_caches()
