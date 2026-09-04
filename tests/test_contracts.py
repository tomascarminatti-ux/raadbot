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

def test_contract_caching_and_mtime_invalidation():
    """Verify that contract loading is cached and invalidated on mtime change."""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)
    initial_contract = {"field1": "string"}

    with open(contract_path, "w") as f:
        json.dump(initial_contract, f)

    _load_contract_cached.cache_clear()

    # First call: cache miss
    data_valid = {"field1": "hello"}
    assert validate_contract(data_valid, contract_path) is True
    hits_1 = _load_contract_cached.cache_info().hits

    # Second call: cache hit
    assert validate_contract(data_valid, contract_path) is True
    hits_2 = _load_contract_cached.cache_info().hits
    assert hits_2 == hits_1 + 1

    # Update file and modify mtime
    updated_contract = {"field1": "string", "field2": "number"}
    with open(contract_path, "w") as f:
        json.dump(updated_contract, f)
    new_time = time.time() + 10
    os.utime(contract_path, (new_time, new_time))

    # Should check new schema (requiring field2)
    assert validate_contract(data_valid, contract_path) is False
    assert validate_contract({"field1": "hello", "field2": 42}, contract_path) is True

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)
