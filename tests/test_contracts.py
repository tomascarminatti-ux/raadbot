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

def test_validate_contract_caching():
    """Verify that caching works and invalidates when contract file changes."""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    # Contract v1: requires "name" (string)
    with open(contract_path, "w") as f:
        json.dump({"name": "string"}, f)

    data = {"name": "Alice"}
    assert validate_contract(data, contract_path) is True

    # Contract v2: requires "name" (string) and "age" (number)
    with open(contract_path, "w") as f:
        json.dump({"name": "string", "age": "number"}, f)

    # Touch mtime explicitly to guarantee invalidation if system clock has coarse resolution
    st = os.stat(contract_path)
    os.utime(contract_path, (st.st_atime, st.st_mtime + 2))

    # Validation against old schema data should fail now
    assert validate_contract(data, contract_path) is False

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
