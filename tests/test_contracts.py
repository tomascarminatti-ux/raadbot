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
    """Verify that contract schema loading is cached and invalidates on mtime change."""
    _load_contract_cached.cache_clear()
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    contract1 = {"field_a": "string"}
    with open(contract_path, "w") as f:
        json.dump(contract1, f)

    data = {"field_a": "hello"}
    assert validate_contract(data, contract_path) is True

    hits_before = _load_contract_cached.cache_info().hits
    assert validate_contract(data, contract_path) is True
    hits_after = _load_contract_cached.cache_info().hits
    assert hits_after == hits_before + 1

    # Invalidate cache by updating contract file and mtime
    contract2 = {"field_b": "number"}
    with open(contract_path, "w") as f:
        json.dump(contract2, f)

    # Ensure mtime is different
    new_mtime = os.path.getmtime(contract_path) + 1.0
    os.utime(contract_path, (new_mtime, new_mtime))

    # Validation against old schema field_a should now fail because schema reloaded field_b
    assert validate_contract(data, contract_path) is False
    assert validate_contract({"field_b": 42}, contract_path) is True

    if os.path.exists(contract_path):
        os.remove(contract_path)
