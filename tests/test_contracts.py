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
    """Verify LRU caching and modification-time (mtime) invalidation for contract loading"""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    initial_contract = {"title": "string"}
    with open(contract_path, "w") as f:
        json.dump(initial_contract, f)

    data = {"title": "Developer"}
    assert validate_contract(data, contract_path) is True

    hits_before = _load_contract_cached.cache_info().hits
    # Second validation should use cached contract
    assert validate_contract(data, contract_path) is True
    hits_after = _load_contract_cached.cache_info().hits
    assert hits_after > hits_before

    # Modify contract file and update mtime to test cache invalidation
    updated_contract = {"title": "string", "age": "number"}
    with open(contract_path, "w") as f:
        json.dump(updated_contract, f)
    # Touch mtime to guarantee new timestamp
    new_time = time.time() + 10
    os.utime(contract_path, (new_time, new_time))

    # Data missing 'age' should fail now because contract was reloaded
    assert validate_contract(data, contract_path) is False

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)
