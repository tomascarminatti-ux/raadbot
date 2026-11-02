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
    """Verify LRU caching and safe cache invalidation on file update."""
    contract_path = "tests/test_cache_contract.json"
    initial_schema = {"field_a": "string"}
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(initial_schema, f)

    try:
        _load_contract_cached.cache_clear()
        initial_info = _load_contract_cached.cache_info()
        assert initial_info.hits == 0
        assert initial_info.misses == 0

        # First call: cache miss
        assert validate_contract({"field_a": "hello"}, contract_path) is True
        info_after_first = _load_contract_cached.cache_info()
        assert info_after_first.hits == 0
        assert info_after_first.misses == 1

        # Second call: cache hit
        assert validate_contract({"field_a": "world"}, contract_path) is True
        info_after_second = _load_contract_cached.cache_info()
        assert info_after_second.hits == 1
        assert info_after_second.misses == 1

        # Update contract on disk and update modification time
        time.sleep(0.01)
        updated_schema = {"field_b": "number"}
        with open(contract_path, "w", encoding="utf-8") as f:
            json.dump(updated_schema, f)
        # Force a forward mtime change to guarantee invalidation
        curr_mtime = os.path.getmtime(contract_path)
        os.utime(contract_path, (curr_mtime + 5, curr_mtime + 5))

        # Old field_a is no longer required, new field_b is required
        assert validate_contract({"field_b": 42}, contract_path) is True
        assert validate_contract({"field_a": "text"}, contract_path) is False

        info_after_update = _load_contract_cached.cache_info()
        # Cache miss triggered by mtime change
        assert info_after_update.misses == 2
        # And subsequent call hit the new cached entry
        assert info_after_update.hits == 2
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
        _load_contract_cached.cache_clear()
