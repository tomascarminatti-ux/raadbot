import os
import json
import pytest
from utils.gem_core import validate_contract, _load_contract_cached
from agent.prompt_builder import load_prompt, build_prompt, clear_prompt_caches, _load_prompt_cached

def test_contract_caching_and_invalidation():
    contract_path = "tests/temp_test_contract.json"

    # 1. Create a temporary contract
    contract_v1 = {
        "status": "string",
        "score": "number"
    }
    with open(contract_path, "w") as f:
        json.dump(contract_v1, f)

    try:
        # 2. Validate valid data under v1
        valid_v1 = {"status": "OK", "score": 0.9}
        assert validate_contract(valid_v1, contract_path) is True

        # 3. Modify the contract on disk (v2)
        contract_v2 = {
            "status": "string",
            "score": "number",
            "required_field": "boolean"
        }

        # Delay briefly to ensure mtime changes
        import time
        time.sleep(0.01)

        with open(contract_path, "w") as f:
            json.dump(contract_v2, f)

        # 4. Check if the validation correctly catches the change (re-evaluates with v2 because of mtime)
        # Should return False now because "required_field" is missing from valid_v1
        assert validate_contract(valid_v1, contract_path) is False

        # 5. Provide required field, now should be True
        valid_v2 = {"status": "OK", "score": 0.9, "required_field": True}
        assert validate_contract(valid_v2, contract_path) is True

    finally:
        # Cleanup
        if os.path.exists(contract_path):
            os.remove(contract_path)

def test_prompt_caching_and_clear():
    # Load prompt and build prompt to populate cache
    prompt_name = "gem1"

    prompt_content = load_prompt(prompt_name)
    assert len(prompt_content) > 0

    # Check cache is populated
    assert _load_prompt_cached.cache_info().hits >= 0

    # Clear cache
    clear_prompt_caches()

    # Hits should reset
    info = _load_prompt_cached.cache_info()
    assert info.currsize == 0
