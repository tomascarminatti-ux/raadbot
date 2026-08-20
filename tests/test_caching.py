import os
import time
import json
import pytest
from agent.prompt_builder import load_prompt
from utils.gem_core import validate_contract

def test_prompt_caching_and_invalidation(tmp_path):
    # Setup temporary prompt file in prompts directory or mock
    prompt_dir = "prompts"
    temp_prompt_file = os.path.join(prompt_dir, "temp_test_gem.md")

    try:
        # Initial write
        with open(temp_prompt_file, "w", encoding="utf-8") as f:
            f.write("Initial prompt content {{input}}")

        # First load
        content1 = load_prompt("temp_test_gem")
        assert content1 == "Initial prompt content {{input}}"

        # Second load (should hit cache)
        content2 = load_prompt("temp_test_gem")
        assert content2 == "Initial prompt content {{input}}"

        # Update file on disk and update mtime using os.utime
        with open(temp_prompt_file, "w", encoding="utf-8") as f:
            f.write("Updated prompt content {{input}}")

        # Explicitly advance mtime to avoid filesystem timestamp granularity issues
        current_mtime = os.path.getmtime(temp_prompt_file)
        os.utime(temp_prompt_file, (current_mtime + 5, current_mtime + 5))

        # Load again (should fetch updated content due to mtime change)
        content3 = load_prompt("temp_test_gem")
        assert content3 == "Updated prompt content {{input}}"

    finally:
        if os.path.exists(temp_prompt_file):
            os.remove(temp_prompt_file)


def test_contract_caching_and_invalidation(tmp_path):
    contract_file = os.path.join("contracts", "temp_test_contract.json")

    try:
        # Initial schema write
        initial_schema = {"name": "string", "score": "number"}
        with open(contract_file, "w", encoding="utf-8") as f:
            json.dump(initial_schema, f)

        valid_data = {"name": "Test", "score": 10}
        assert validate_contract(valid_data, contract_file) is True

        # Update schema to require a new field
        updated_schema = {"name": "string", "score": "number", "required_flag": "boolean"}
        with open(contract_file, "w", encoding="utf-8") as f:
            json.dump(updated_schema, f)

        # Explicitly advance mtime to ensure cache invalidation
        current_mtime = os.path.getmtime(contract_file)
        os.utime(contract_file, (current_mtime + 5, current_mtime + 5))

        # With updated schema, valid_data missing 'required_flag' should fail contract validation
        assert validate_contract(valid_data, contract_file) is False

    finally:
        if os.path.exists(contract_file):
            os.remove(contract_file)
