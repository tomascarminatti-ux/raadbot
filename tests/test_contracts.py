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
    """Verify contract caching and invalidation on file modification."""
    import time
    from utils.gem_core import _load_contract_cached

    contract_path = "tests/temp_cache_contract.json"
    schema_v1 = {"title": "string", "count": "number"}
    schema_v2 = {"title": "string", "verified": "boolean"}

    try:
        with open(contract_path, "w", encoding="utf-8") as f:
            json.dump(schema_v1, f)

        # First validation - populates cache
        valid_v1 = {"title": "Test", "count": 10}
        invalid_v1 = {"title": "Test", "verified": True}
        assert validate_contract(valid_v1, contract_path) is True
        assert validate_contract(invalid_v1, contract_path) is False

        # Check cache hits increment
        info_before = _load_contract_cached.cache_info()
        assert validate_contract(valid_v1, contract_path) is True
        info_after = _load_contract_cached.cache_info()
        assert info_after.hits > info_before.hits

        # Invalidate by updating contract file and its timestamp
        time.sleep(0.02)
        with open(contract_path, "w", encoding="utf-8") as f:
            json.dump(schema_v2, f)
        # Ensure timestamp changed
        curr_mtime = os.stat(contract_path).st_mtime
        os.utime(contract_path, (curr_mtime + 1, curr_mtime + 1))

        # Schema v2 now active
        valid_v2 = {"title": "Test", "verified": True}
        invalid_v2 = {"title": "Test", "count": 10}
        assert validate_contract(valid_v2, contract_path) is True
        assert validate_contract(invalid_v2, contract_path) is False
    finally:
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
