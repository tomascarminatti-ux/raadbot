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
    """Verify that contract schema caching works and invalidates when file mtime changes."""
    from utils.gem_core import _load_contract_cached, validate_contract

    _load_contract_cached.cache_clear()
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    contract1 = {"field_a": "string"}
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract1, f)

    data1 = {"field_a": "hello"}
    assert validate_contract(data1, contract_path) is True

    hits_before = _load_contract_cached.cache_info().hits
    # Second call with same mtime should hit cache
    assert validate_contract(data1, contract_path) is True
    hits_after = _load_contract_cached.cache_info().hits
    assert hits_after == hits_before + 1

    # Modify file and update mtime to trigger cache invalidation
    contract2 = {"field_a": "string", "field_b": "number"}
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract2, f)
    current_mtime = os.path.getmtime(contract_path)
    os.utime(contract_path, (current_mtime + 10, current_mtime + 10))

    # Old data missing field_b should now fail contract validation
    assert validate_contract(data1, contract_path) is False

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
