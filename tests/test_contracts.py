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


def test_validate_contract_cache_and_invalidation(tmp_path):
    """Verify that validate_contract uses cached contract schema and invalidates cache on file mtime update"""
    from utils.gem_core import _load_contract_cached

    contract_file = tmp_path / "cache_test_contract.json"

    initial_schema = {"field": "string"}
    contract_file.write_text(json.dumps(initial_schema), encoding="utf-8")

    info_before = _load_contract_cached.cache_info()

    data1 = {"field": "hello"}
    assert validate_contract(data1, str(contract_file)) is True

    info_after_first = _load_contract_cached.cache_info()
    assert info_after_first.hits == info_before.hits

    # Second validation call with same file mtime should result in a cache hit
    assert validate_contract(data1, str(contract_file)) is True
    info_after_second = _load_contract_cached.cache_info()
    assert info_after_second.hits == info_after_first.hits + 1

    # Modify schema on disk and update modification time
    updated_schema = {"field": "number"}
    contract_file.write_text(json.dumps(updated_schema), encoding="utf-8")
    new_mtime = os.path.getmtime(contract_file) + 10.0
    os.utime(contract_file, (new_mtime, new_mtime))

    # Validation should now fail because 'field' expects number
    assert validate_contract(data1, str(contract_file)) is False

    data2 = {"field": 123}
    assert validate_contract(data2, str(contract_file)) is True
