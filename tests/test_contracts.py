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


def test_validate_contract_cache_and_invalidation(tmp_path):
    """Verify schema caching and invalidation on modification."""
    from utils.gem_core import _load_contract_cached
    import time

    contract_file = tmp_path / "test_schema.json"
    contract_data = {"status": "string"}
    contract_file.write_text(json.dumps(contract_data))

    _load_contract_cached.cache_clear()
    initial_info = _load_contract_cached.cache_info()

    # First validation -> cache miss
    assert validate_contract({"status": "ok"}, str(contract_file)) is True
    assert _load_contract_cached.cache_info().misses == initial_info.misses + 1
    assert _load_contract_cached.cache_info().hits == initial_info.hits

    # Second validation -> cache hit
    assert validate_contract({"status": "ok"}, str(contract_file)) is True
    assert _load_contract_cached.cache_info().hits == initial_info.hits + 1

    # Modify file and update mtime to test cache invalidation
    time.sleep(0.01)
    new_contract = {"status": "string", "new_field": "number"}
    contract_file.write_text(json.dumps(new_contract))
    # Update access and modification times explicitly
    now = time.time() + 1
    os.utime(str(contract_file), (now, now))

    # Should detect new mtime, miss cache, and require new_field
    assert validate_contract({"status": "ok"}, str(contract_file)) is False
    valid = validate_contract(
        {"status": "ok", "new_field": 42}, str(contract_file)
    )
    assert valid is True
    # The first call after mtime change is a miss, subsequent is a hit
    assert _load_contract_cached.cache_info().misses == initial_info.misses + 2
    assert _load_contract_cached.cache_info().hits == initial_info.hits + 2


def test_real_contracts():
    """Verify that current contracts are valid JSON and can be loaded"""
    contract_dir = "contracts"
    for filename in os.listdir(contract_dir):
        if filename.endswith(".json"):
            path = os.path.join(contract_dir, filename)
            with open(path, "r") as f:
                data = json.load(f)
                assert isinstance(data, dict)
