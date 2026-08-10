import os
import json
from agent.prompt_builder import load_prompt
from utils.gem_core import validate_contract

def test_prompt_cache_and_invalidation():
    # We will test using a temporary prompt file.
    # PROMPTS_DIR is prompts/ so we can write to prompts/temp_test_prompt.md
    temp_prompt_name = "temp_test_prompt"
    temp_filepath = f"prompts/{temp_prompt_name}.md"

    try:
        # 1. Write initial content
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Initial prompt content")

        # 2. First load should return initial content
        p1 = load_prompt(temp_prompt_name)
        assert p1 == "Initial prompt content"

        # 3. Overwrite the file immediately
        with open(temp_filepath, "w", encoding="utf-8") as f:
            f.write("Updated prompt content")

        # Force the mtime forward to ensure the cache invalidates correctly
        orig_mtime = os.path.getmtime(temp_filepath)
        os.utime(temp_filepath, (orig_mtime + 5, orig_mtime + 5))

        # 4. Load again; it should be invalidated and load the updated content
        p2 = load_prompt(temp_prompt_name)
        assert p2 == "Updated prompt content"

    finally:
        if os.path.exists(temp_filepath):
            os.remove(temp_filepath)

def test_contract_cache_and_invalidation():
    temp_contract_path = "tests/temp_test_contract.json"

    try:
        # 1. Write initial schema
        schema_v1 = {"name": "string"}
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            json.dump(schema_v1, f)

        # Validate data against it
        data_valid = {"name": "Test"}
        data_invalid = {"name": 123}

        # This warm-up caches the contract schema
        assert validate_contract(data_valid, temp_contract_path) is True
        assert validate_contract(data_invalid, temp_contract_path) is False

        # 2. Overwrite the schema on disk to change type expectation to number
        schema_v2 = {"name": "number"}
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            json.dump(schema_v2, f)

        # Force mtime forward to guarantee invalidation
        orig_mtime = os.path.getmtime(temp_contract_path)
        os.utime(temp_contract_path, (orig_mtime + 5, orig_mtime + 5))

        # 3. Validate again; since schema is updated and cache invalidated:
        # name="Test" (string) should now be INVALID, and name=123 (number) should be VALID!
        assert validate_contract(data_valid, temp_contract_path) is False
        assert validate_contract(data_invalid, temp_contract_path) is True

    finally:
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)
