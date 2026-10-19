import pytest
import json
import os
import time
from utils.gem_core import validate_contract, _load_contract_cached

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
    """Verify that validate_contract caches schema loading and invalidates cache when mtime changes."""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    # Initial contract
    contract_v1 = {"field": "string"}
    with open(contract_path, "w") as f:
        json.dump(contract_v1, f)

    # Initial validation (cache miss)
    hits_before = _load_contract_cached.cache_info().hits
    assert validate_contract({"field": "hello"}, contract_path) is True

    # Second validation (cache hit)
    assert validate_contract({"field": "world"}, contract_path) is True
    hits_after = _load_contract_cached.cache_info().hits
    assert hits_after > hits_before

    # Update contract schema to require number instead of string
    contract_v2 = {"field": "number"}
    time.sleep(0.01)  # Ensure mtime changes
    with open(contract_path, "w") as f:
        json.dump(contract_v2, f)
    new_mtime = os.path.getmtime(contract_path) + 1.0
    os.utime(contract_path, (new_mtime, new_mtime))

    # Should reload and invalidate cache: string "hello" fails number validation
    assert validate_contract({"field": "hello"}, contract_path) is False
    # Valid number passes
    assert validate_contract({"field": 42}, contract_path) is True

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)
