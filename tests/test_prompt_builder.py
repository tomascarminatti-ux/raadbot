import os
import pytest
from agent.prompt_builder import (
    load_prompt,
    build_prompt,
    get_required_variables,
    clear_prompt_caches,
    PROMPTS_DIR,
)


@pytest.fixture(autouse=True)
def clean_cache():
    clear_prompt_caches()
    yield
    clear_prompt_caches()


def test_load_prompt_cache_and_invalidation():
    temp_gem = "temp_test_prompt"
    filepath = os.path.join(PROMPTS_DIR, f"{temp_gem}.md")

    try:
        # 1. Create initial prompt file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Initial content for {{test_var}}")

        content1 = load_prompt(temp_gem)
        assert content1 == "Initial content for {{test_var}}"

        # 2. Reading again should return cached content
        content2 = load_prompt(temp_gem)
        assert content2 == "Initial content for {{test_var}}"

        # 3. Update file content and update mtime using os.utime to ensure invalidation
        new_mtime = os.path.getmtime(filepath) + 10.0
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Updated content for {{test_var}}")
        os.utime(filepath, (new_mtime, new_mtime))

        content3 = load_prompt(temp_gem)
        assert content3 == "Updated content for {{test_var}}"

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)


def test_build_prompt_and_required_variables():
    temp_gem = "temp_test_prompt_vars"
    filepath = os.path.join(PROMPTS_DIR, f"{temp_gem}.md")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Hello {{name}}, welcome to {{role}}!")

        # Check required variables
        req_vars = get_required_variables(temp_gem)
        assert set(req_vars) == {"name", "role"}

        # Build prompt with test variables
        built = build_prompt(temp_gem, {"name": "Alice", "role": "Engineer"})
        assert "Hello Alice, welcome to Engineer!" in built

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
