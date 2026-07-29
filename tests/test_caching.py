import os
import time
import json
import pytest
from utils.gem_core import validate_contract
from agent.prompt_builder import load_prompt

def test_contract_caching_and_invalidation():
    # Create a temporary contract
    temp_contract_path = "tests/temp_test_contract.json"

    # 1. Write initial contract
    with open(temp_contract_path, "w", encoding="utf-8") as f:
        json.dump({"field1": "string"}, f)

    try:
        # Validate data with original schema
        assert validate_contract({"field1": "hello"}, temp_contract_path) is True
        assert validate_contract({"field1": 123}, temp_contract_path) is False

        # 2. Modify the contract on disk
        # Make sure to wait a moment or explicitly alter mtime to ensure it changes
        time.sleep(0.01)
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            json.dump({"field1": "number"}, f)

        # Clear or force update mtime
        # Since we modified the file, mtime is updated. Let's check if invalidation worked:
        assert validate_contract({"field1": 123}, temp_contract_path) is True
        assert validate_contract({"field1": "hello"}, temp_contract_path) is False

    finally:
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)


def test_prompt_caching_and_invalidation():
    temp_prompt_path = os.path.join("prompts", "temp_prompt.md")

    # 1. Write initial prompt
    with open(temp_prompt_path, "w", encoding="utf-8") as f:
        f.write("Initial prompt content")

    try:
        # Load prompt and assert contents
        assert load_prompt("temp_prompt") == "Initial prompt content"

        # 2. Modify prompt on disk
        time.sleep(0.01)
        with open(temp_prompt_path, "w", encoding="utf-8") as f:
            f.write("Updated prompt content")

        # Asserts cache invalidation based on file modification time
        assert load_prompt("temp_prompt") == "Updated prompt content"

    finally:
        if os.path.exists(temp_prompt_path):
            os.remove(temp_prompt_path)
