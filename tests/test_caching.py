import os
import json
import time
import pytest
from agent.prompt_builder import load_prompt, _load_prompt_cached, PROMPTS_DIR
from utils.gem_core import validate_contract, _load_contract_cached


def test_prompt_caching_and_invalidation(tmp_path):
    # Setup temporary prompt file in PROMPTS_DIR to be loaded by load_prompt
    # Since load_prompt is hardcoded to look in PROMPTS_DIR, we can write a test prompt file there
    test_gem_name = "test_prompt_caching_temp"
    test_filepath = os.path.join(PROMPTS_DIR, f"{test_gem_name}.md")

    try:
        # 1. Write initial content
        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write("Initial Content")

        # Load initially
        content1 = load_prompt(test_gem_name)
        assert content1 == "Initial Content"

        # 2. Modify file content but KEEP the same mtime (or very similar)
        # To make sure we test mtime, let's explicitly set the mtime
        initial_mtime = os.path.getmtime(test_filepath)

        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write("Modified Content")

        # Reset mtime back to original to simulate checking cache hit
        os.utime(test_filepath, (initial_mtime, initial_mtime))

        content2 = load_prompt(test_gem_name)
        # It should hit the cache and return the old content because mtime didn't change!
        assert content2 == "Initial Content"

        # 3. Change mtime to simulate invalidation (forward in time)
        future_mtime = initial_mtime + 5.0
        os.utime(test_filepath, (future_mtime, future_mtime))

        content3 = load_prompt(test_gem_name)
        # It should recognize the changed mtime and load the new content!
        assert content3 == "Modified Content"

    finally:
        if os.path.exists(test_filepath):
            os.remove(test_filepath)


def test_contract_caching_and_invalidation(tmp_path):
    contract_path = str(tmp_path / "test_contract.json")

    # 1. Write initial contract
    contract1 = {
        "status": "string"
    }
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract1, f)

    initial_mtime = os.path.getmtime(contract_path)

    # Validate should succeed for {"status": "ok"}
    assert validate_contract({"status": "ok"}, contract_path) is True
    # Validate should fail for {"status": 123}
    assert validate_contract({"status": 123}, contract_path) is False

    # 2. Modify contract but KEEP the same mtime
    contract2 = {
        "status": "number"
    }
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract2, f)
    os.utime(contract_path, (initial_mtime, initial_mtime))

    # Due to caching (mtime same), validating {"status": "ok"} should still be True
    assert validate_contract({"status": "ok"}, contract_path) is True
    assert validate_contract({"status": 123}, contract_path) is False

    # 3. Modify mtime to trigger invalidation
    future_mtime = initial_mtime + 5.0
    os.utime(contract_path, (future_mtime, future_mtime))

    # Now it should reload contract2 and validating {"status": 123} should be True, and "ok" should be False
    assert validate_contract({"status": 123}, contract_path) is True
    assert validate_contract({"status": "ok"}, contract_path) is False
