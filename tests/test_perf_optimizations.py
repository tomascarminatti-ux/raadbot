import os
import json
import time
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_caches
from utils.gem_core import validate_contract

def test_prompt_cache_and_invalidation():
    # Setup test file
    test_gem = "temp_test_gem"
    prompt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts")
    os.makedirs(prompt_dir, exist_ok=True)
    test_filepath = os.path.join(prompt_dir, f"{test_gem}.md")

    try:
        # 1. Write initial prompt content
        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write("Initial prompt content: {{input}}")

        # 2. First load
        content1 = load_prompt(test_gem)
        assert content1 == "Initial prompt content: {{input}}"

        # 3. Modify file content but with NO sleep (mtime might be the same if it happens too fast)
        # To simulate a disk change correctly we write a new content and update its mtime explicitly
        # incrementing by 5 seconds to ensure mtime detects it
        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write("Updated prompt content: {{input}}")

        current_mtime = os.path.getmtime(test_filepath)
        os.utime(test_filepath, (current_mtime + 5, current_mtime + 5))

        # 4. Load again and assert it invalidates and loads the new content
        content2 = load_prompt(test_gem)
        assert content2 == "Updated prompt content: {{input}}"

        # 5. Test manual clear cache
        with open(test_filepath, "w", encoding="utf-8") as f:
            f.write("Manually cleared content: {{input}}")

        clear_prompt_caches()
        content3 = load_prompt(test_gem)
        assert content3 == "Manually cleared content: {{input}}"

    finally:
        if os.path.exists(test_filepath):
            os.remove(test_filepath)


def test_contract_cache_and_invalidation():
    # Setup test file
    test_contract_path = "tests/temp_test_contract_opt.json"

    try:
        # 1. Write initial contract
        contract1 = {"field": "string"}
        with open(test_contract_path, "w") as f:
            json.dump(contract1, f)

        # 2. Validate valid and invalid data
        assert validate_contract({"field": "hello"}, test_contract_path) is True
        assert validate_contract({"field": 123}, test_contract_path) is False

        # 3. Update contract on disk and adjust mtime to force invalidation
        contract2 = {"field": "number"}
        with open(test_contract_path, "w") as f:
            json.dump(contract2, f)

        current_mtime = os.path.getmtime(test_contract_path)
        os.utime(test_contract_path, (current_mtime + 5, current_mtime + 5))

        # 4. Validate again - now the expectation has inverted because type is number
        assert validate_contract({"field": "hello"}, test_contract_path) is False
        assert validate_contract({"field": 123}, test_contract_path) is True

    finally:
        if os.path.exists(test_contract_path):
            os.remove(test_contract_path)
