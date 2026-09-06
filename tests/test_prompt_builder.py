import os
import time
import pytest
from agent.prompt_builder import load_prompt, build_prompt, get_required_variables, PROMPTS_DIR, _load_prompt_cached

def test_prompt_builder_cache_and_invalidation():
    temp_gem_name = "temp_test_prompt"
    temp_filepath = os.path.join(PROMPTS_DIR, f"{temp_gem_name}.md")

    try:
        # 1. Create initial prompt
        initial_content = "Hello {{name}}, welcome to {{service}}!"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write(initial_content)

        # Clear cache prior to initial read
        _load_prompt_cached.cache_clear()

        content_v1 = load_prompt(temp_gem_name)
        assert content_v1 == initial_content

        info1 = _load_prompt_cached.cache_info()
        assert info1.hits == 0
        assert info1.misses >= 1

        # Second call should hit cache
        content_v1_again = load_prompt(temp_gem_name)
        assert content_v1_again == initial_content
        info2 = _load_prompt_cached.cache_info()
        assert info2.hits >= 1

        # 2. Modify file and update mtime using os.utime for deterministic testing
        updated_content = "Updated {{name}} for {{service}}!"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)

        current_mtime = os.path.getmtime(temp_filepath)
        os.utime(temp_filepath, (current_mtime + 10, current_mtime + 10))

        content_v2 = load_prompt(temp_gem_name)
        assert content_v2 == updated_content

    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

def test_build_prompt_and_get_required_variables():
    temp_gem_name = "temp_var_test"
    temp_filepath = os.path.join(PROMPTS_DIR, f"{temp_gem_name}.md")

    try:
        content = "System: {{PROMPT_MAESTRO}}\nUser: {{user_val}}\nMetadata: {{VERSION}}"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write(content)

        required_vars = get_required_variables(temp_gem_name)
        assert required_vars == ["user_val"]

        built = build_prompt(temp_gem_name, {"user_val": "Alice"})
        assert "User: Alice" in built
        assert "{{PROMPT_MAESTRO}}" not in built
    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
