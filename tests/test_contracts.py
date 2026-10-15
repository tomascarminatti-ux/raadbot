import pytest
import json
import os
import time
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
    """Verify that validate_contract caches contract reads and invalidates on mtime change."""
    contract_path = "tests/temp_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    initial_contract = {"field_a": "string"}
    with open(contract_path, "w") as f:
        json.dump(initial_contract, f)

    try:
        # First call loads and caches initial schema
        assert validate_contract({"field_a": "hello"}, contract_path) is True
        assert validate_contract({"field_a": 123}, contract_path) is False

        # Modify contract file on disk
        updated_contract = {"field_a": "string", "field_b": "number"}
        time.sleep(0.01)  # Ensure distinct mtime
        with open(contract_path, "w") as f:
            json.dump(updated_contract, f)

        # Explicitly update mtime so caching key changes
        now = time.time() + 1.0
        os.utime(contract_path, (now, now))

        # New call should detect changed mtime, reload updated contract, and enforce field_b
        assert validate_contract({"field_a": "hello"}, contract_path) is False
        assert validate_contract({"field_a": "hello", "field_b": 42}, contract_path) is True
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
