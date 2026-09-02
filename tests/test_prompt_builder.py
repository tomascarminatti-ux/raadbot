import os

from agent.prompt_builder import (
    build_prompt,
    clear_prompt_caches,
    get_required_variables,
    load_prompt,
)


def test_load_prompt_and_cache():
    # Clear cache first
    clear_prompt_caches()

    # Load prompt maestro
    content1 = load_prompt("00_prompt_maestro")
    assert isinstance(content1, str)
    assert len(content1) > 0

    # Verify cache info shows a hit on second call
    cache_info_before = load_prompt.cache_info()
    content2 = load_prompt("00_prompt_maestro")
    cache_info_after = load_prompt.cache_info()

    assert content1 == content2
    assert cache_info_after.hits > cache_info_before.hits

    # Test cache clear
    clear_prompt_caches()
    cache_info_cleared = load_prompt.cache_info()
    assert cache_info_cleared.hits == 0


def test_build_prompt_and_variables(tmp_path):
    # Test using temporary test prompt file in prompts directory
    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    temp_file = os.path.join(prompts_dir, "temp_test_prompt.md")

    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(
                "Hello {{name}}, welcome to {{company}}! Maestro: {{PROMPT_MAESTRO}}"
            )

        clear_prompt_caches()

        # Test get_required_variables
        req_vars = get_required_variables("temp_test_prompt")
        assert "name" in req_vars
        assert "company" in req_vars
        assert "PROMPT_MAESTRO" not in req_vars

        # Test build_prompt
        built = build_prompt(
            "temp_test_prompt", {"name": "Alice", "company": "Acme Corp"}
        )
        assert "Hello Alice, welcome to Acme Corp!" in built
        assert "{{name}}" not in built
        assert "{{company}}" not in built

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
        clear_prompt_caches()
