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
    """Test contract loading caching and invalidation when file mtime changes"""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    # Contract v1
    contract_v1 = {"field1": "string"}
    with open(contract_path, "w") as f:
        json.dump(contract_v1, f)

    data_v1 = {"field1": "value"}
    data_v2 = {"field1": "value", "field2": "value"}

    assert validate_contract(data_v1, contract_path) is True
    assert validate_contract(data_v2, contract_path) is True  # missing field2 in contract v1, passes

    # Update contract v2 with field2 required
    import time
    time.sleep(0.01) # ensure mtime timestamp differs
    contract_v2 = {"field1": "string", "field2": "string"}
    with open(contract_path, "w") as f:
        json.dump(contract_v2, f)

    # Now data_v1 should fail because field2 is required in v2
    assert validate_contract(data_v1, contract_path) is False
    assert validate_contract(data_v2, contract_path) is True

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)
