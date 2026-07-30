import os
import pytest
from agent.prompt_builder import load_prompt, clear_prompt_cache
from utils.gem_core import validate_contract, _load_contract

def test_prompt_caching_and_invalidation():
    temp_prompt_name = "temp_test_prompt"
    temp_prompt_path = "prompts/temp_test_prompt.md"

    # 1. Ensure any previous temp file is gone
    if os.path.exists(temp_prompt_path):
        os.remove(temp_prompt_path)
    clear_prompt_cache()

    # Write initial content
    with open(temp_prompt_path, "w", encoding="utf-8") as f:
        f.write("Initial content")

    try:
        # Load first time (reads from disk)
        content_1 = load_prompt(temp_prompt_name)
        assert content_1 == "Initial content"

        # Modify the file on disk
        with open(temp_prompt_path, "w", encoding="utf-8") as f:
            f.write("Modified content")

        # Load second time (should hit cache and return initial content)
        content_2 = load_prompt(temp_prompt_name)
        assert content_2 == "Initial content"

        # Clear cache and load third time (should fetch modified content from disk)
        clear_prompt_cache()
        content_3 = load_prompt(temp_prompt_name)
        assert content_3 == "Modified content"

    finally:
        # Cleanup
        if os.path.exists(temp_prompt_path):
            os.remove(temp_prompt_path)
        clear_prompt_cache()

def test_contract_caching():
    temp_contract_path = "contracts/temp_test_contract.json"

    if os.path.exists(temp_contract_path):
        os.remove(temp_contract_path)
    _load_contract.cache_clear()

    # Write initial schema
    with open(temp_contract_path, "w", encoding="utf-8") as f:
        f.write('{"field": "string"}')

    try:
        # Validate data
        res_1 = validate_contract({"field": "hello"}, temp_contract_path)
        assert res_1 is True

        # Modify schema on disk to make validation fail
        with open(temp_contract_path, "w", encoding="utf-8") as f:
            f.write('{"field": "number"}')

        # Validation should still succeed because the old contract is cached
        res_2 = validate_contract({"field": "hello"}, temp_contract_path)
        assert res_2 is True

        # Clear cache and validate again
        _load_contract.cache_clear()
        res_3 = validate_contract({"field": "hello"}, temp_contract_path)
        assert res_3 is False  # Now it should be loaded from disk and fail (since field should be a number)

    finally:
        if os.path.exists(temp_contract_path):
            os.remove(temp_contract_path)
        _load_contract.cache_clear()
