import pytest
import json
import os
from utils.gem_core import validate_contract

def test_validate_contract_types():
    # Create temp contract
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object"
    }
    contract_path = "tests/temp_contract.json"
    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)
    
    # Valid data
    valid_data = {
        "name": "Test",
        "score": 0.9,
        "is_active": True,
        "tags": ["a", "b"],
        "metadata": {"key": "value"}
    }
    assert validate_contract(valid_data, contract_path) is True
    
    # Invalid type
    invalid_data = valid_data.copy()
    invalid_data["score"] = "high"
    assert validate_contract(invalid_data, contract_path) is False
    
    # Missing key
    missing_data = valid_data.copy()
    missing_data.pop("name", None)
    assert validate_contract(missing_data, contract_path) is False

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)

def test_real_contracts():
    """Verify that current contracts are valid JSON and can be loaded"""
    contract_dir = "contracts"
    for filename in os.listdir(contract_dir):
        if filename.endswith(".json"):
            path = os.path.join(contract_dir, filename)
            with open(path, "r") as f:
                data = json.load(f)
                assert isinstance(data, dict)


def test_validate_contract_cache_and_invalidation():
    """Verify LRU caching and mtime-based invalidation for validate_contract"""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)
    try:
        # Contract v1: requires 'name'
        with open(contract_path, "w") as f:
            json.dump({"name": "string"}, f)

        data = {"name": "Alice"}
        assert validate_contract(data, contract_path) is True

        # Contract v2: updated to require 'extra_field'
        with open(contract_path, "w") as f:
            json.dump({"name": "string", "extra_field": "string"}, f)

        # Update mtime explicitly using os.utime
        mtime = os.path.getmtime(contract_path) + 10.0
        os.utime(contract_path, (mtime, mtime))

        # Should fail as cache invalidates and reads updated contract
        assert validate_contract(data, contract_path) is False
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
