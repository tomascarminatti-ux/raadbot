import os
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    clear_prompt_caches,
    PROMPTS_DIR,
)


def test_load_prompt_caching_and_invalidation():
    # Clear cache before starting
    clear_prompt_caches()

    # Load prompt for gem5
    prompt_initial = load_prompt("gem5")
    info1 = load_prompt.cache_info()
    assert info1.hits == 0

    # Second call should hit the LRU cache
    prompt_cached = load_prompt("gem5")
    info2 = load_prompt.cache_info()
    assert info2.hits == 1
    assert prompt_initial == prompt_cached

    # Clear cache and check info
    clear_prompt_caches()
    info3 = load_prompt.cache_info()
    assert info3.hits == 0


def test_build_prompt_with_cached_templates():
    clear_prompt_caches()
    temp_file = os.path.join(PROMPTS_DIR, "temp_test_prompt.md")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write("Hola {{role_name}} en {{location_name}}. {{PROMPT_MAESTRO}}")

        variables = {
            "role_name": "Developer",
            "location_name": "Madrid",
        }
        prompt = build_prompt("temp_test_prompt", variables)
        assert "Developer" in prompt
        assert "Madrid" in prompt
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        clear_prompt_caches()


def test_get_required_variables_caching():
    clear_prompt_caches()
    temp_file = os.path.join(PROMPTS_DIR, "temp_test_prompt.md")
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write("Role: {{role_name}}, Location: {{location_name}}, Master: {{PROMPT_MAESTRO}}, Version: {{VERSION}}")

        vars1 = get_required_variables("temp_test_prompt")
        info1 = load_prompt.cache_info()
        assert set(vars1) == {"role_name", "location_name"}

        vars2 = get_required_variables("temp_test_prompt")
        info2 = load_prompt.cache_info()
        assert info2.hits >= info1.hits + 1
        assert set(vars2) == set(vars1)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        clear_prompt_caches()
