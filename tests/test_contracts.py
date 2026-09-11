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

def test_validate_contract_cache_and_invalidation():
    from utils.gem_core import _load_contract_cached
    _load_contract_cached.cache_clear()

    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    with open(contract_path, "w") as f:
        json.dump({"field": "string"}, f)

    data = {"field": "hello"}

    # First validation populates cache
    assert validate_contract(data, contract_path) is True
    hits_before = _load_contract_cached.cache_info().hits

    # Second validation hits cache
    assert validate_contract(data, contract_path) is True
    assert _load_contract_cached.cache_info().hits == hits_before + 1

    # Modify file content and explicit mtime update
    with open(contract_path, "w") as f:
        json.dump({"field": "number"}, f)
    mtime_now = os.path.getmtime(contract_path)
    os.utime(contract_path, (mtime_now + 10, mtime_now + 10))

    # Now validation with same data fails because schema expected number
    assert validate_contract(data, contract_path) is False

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
