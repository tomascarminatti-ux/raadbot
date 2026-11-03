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
    """Verify _load_contract_cached caches results and invalidates on mtime"""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)
    _load_contract_cached.cache_clear()

    try:
        # Create initial contract
        with open(contract_path, "w") as f:
            json.dump({"field1": "string"}, f)

        data1 = {"field1": "valid"}
        data2 = {"field1": "valid", "field2": "valid"}

        # First validation - initial cache miss
        assert validate_contract(data1, contract_path) is True
        info_before = _load_contract_cached.cache_info()
        assert info_before.currsize >= 1

        # Second validation - should hit cache
        assert validate_contract(data1, contract_path) is True
        info_after = _load_contract_cached.cache_info()
        assert info_after.hits == info_before.hits + 1

        # Sleep briefly to ensure new mtime timestamp
        time.sleep(0.05)
        # Update contract to require field2
        with open(contract_path, "w") as f:
            json.dump({"field1": "string", "field2": "string"}, f)

        # data1 should now fail validation because of updated contract schema
        assert validate_contract(data1, contract_path) is False
        # data2 has both fields, should be valid
        assert validate_contract(data2, contract_path) is True
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
