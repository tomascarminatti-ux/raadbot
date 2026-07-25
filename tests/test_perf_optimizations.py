import os
import json
import time
import pytest
from agent.prompt_builder import build_prompt, load_prompt, clear_prompt_caches
from utils.gem_core import validate_contract, clear_contract_caches

def test_prompt_cache_invalidation():
    # Setup a temp prompt file
    temp_prompt_name = "test_temp_prompt"
    temp_filepath = "prompts/test_temp_prompt.md"

    with open(temp_filepath, "w", encoding="utf-8") as f:
        f.write("Initial prompt content {{input}}")

    try:
        # Clear caches first
        clear_prompt_caches()

        # Load initially
        content_1 = load_prompt(temp_prompt_name)
        assert content_1 == "Initial prompt content {{input}}"

        # Sleep slightly to ensure mtime changes if we overwrite
        time.sleep(0.01)

        # Overwrite file
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Updated prompt content {{input}}")

        # Loading again should automatically notice the new mtime and return updated content
        content_2 = load_prompt(temp_prompt_name)
        assert content_2 == "Updated prompt content {{input}}"

    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

def test_contract_cache_invalidation():
    temp_contract_path = "contracts/test_temp_contract.schema.json"

    contract_1 = {
        "score": "number"
    }

    with open(temp_contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_1, f)

    try:
        clear_contract_caches()

        # Check validation with first schema
        assert validate_contract({"score": 95}, temp_contract_path) is True
        assert validate_contract({"name": "No score"}, temp_contract_path) is False

        time.sleep(0.01)

        # Overwrite with a different schema requiring "name"
        contract_2 = {
            "name": "string"
        }
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            json.dump(contract_2, f)

        # It should automatically invalidate and use the new schema
        assert validate_contract({"score": 95}, temp_contract_path) is False
        assert validate_contract({"name": "John"}, temp_contract_path) is True

    finally:
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)
