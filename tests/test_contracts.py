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

def test_validate_contract_cache_performance():
    """Verify caching hit and measure execution performance for validate_contract."""
    from utils.gem_core import _load_contract_cached
    _load_contract_cached.cache_clear()

    contract = {"name": "string", "score": "number"}
    contract_path = "tests/temp_perf_contract.json"
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    try:
        valid_data = {"name": "Test", "score": 10}

        # First call loads contract into cache
        assert validate_contract(valid_data, contract_path) is True
        info1 = _load_contract_cached.cache_info()
        assert info1.hits == 0
        assert info1.misses >= 1

        # Subsequent calls hit LRU cache
        for _ in range(100):
            assert validate_contract(valid_data, contract_path) is True

        info2 = _load_contract_cached.cache_info()
        assert info2.hits >= 100
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
