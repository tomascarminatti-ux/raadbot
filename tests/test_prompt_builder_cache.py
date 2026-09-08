import os
import time
from agent.prompt_builder import (
    PROMPTS_DIR,
    _load_prompt_cached,
    build_prompt,
    clear_prompt_caches,
    get_required_variables,
    load_prompt,
)


def test_prompt_caching_and_invalidation():
    clear_prompt_caches()

    # Create a temporary test prompt file in PROMPTS_DIR to avoid mutating production prompt files
    temp_prompt_name = "temp_test_prompt"
    temp_filepath = os.path.join(PROMPTS_DIR, f"{temp_prompt_name}.md")

    initial_content = "Hello {{candidate_name}}, welcome to {{company_name}}!"
    with open(temp_filepath, "w", encoding="utf-8") as f:
        f.write(initial_content)

    try:
        # Initial load
        content1 = load_prompt(temp_prompt_name)
        assert content1 == initial_content

        cache_info1 = _load_prompt_cached.cache_info()
        assert cache_info1.hits == 0

        # Second load should hit cache
        content2 = load_prompt(temp_prompt_name)
        assert content2 == initial_content

        cache_info2 = _load_prompt_cached.cache_info()
        assert cache_info2.hits >= 1

        # Test building prompt
        built = build_prompt(
            temp_prompt_name,
            {"candidate_name": "Alice", "company_name": "Acme Corp"},
        )
        assert "Hello Alice, welcome to Acme Corp!" in built

        # Test required variables
        req_vars = get_required_variables(temp_prompt_name)
        assert set(req_vars) == {"candidate_name", "company_name"}

        # Modify file and update mtime to trigger cache invalidation
        updated_content = "Greetings {{candidate_name}}, welcome to {{company_name}}!"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write(updated_content)

        stat = os.stat(temp_filepath)
        os.utime(temp_filepath, (stat.st_atime, stat.st_mtime + 5))

        # Reloading after file update should return updated content
        content3 = load_prompt(temp_prompt_name)
        assert content3 == updated_content

    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)
        clear_prompt_caches()
