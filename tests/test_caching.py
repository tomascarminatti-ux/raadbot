import os
import json
from utils.gem_core import validate_contract, _load_contract_cached

def test_contract_caching_correctness():
    """Verify that contract schema caching is fast, correct, and correctly invalidated on disk changes."""
    contract_path = "tests/temp_test_caching_contract.json"

    # 1. Write initial contract
    contract_1 = {"name": "string"}
    with open(contract_path, "w") as f:
        json.dump(contract_1, f)

    try:
        # Clear cache first to ensure a deterministic test start
        _load_contract_cached.cache_clear()

        # Validate data against contract_1
        assert validate_contract({"name": "test"}, contract_path) is True
        assert validate_contract({"age": 42}, contract_path) is False

        # Get cache info
        hits_before = _load_contract_cached.cache_info().hits

        # Call validate_contract again (should be a cache hit)
        assert validate_contract({"name": "test2"}, contract_path) is True

        # Confirm cache hit occurred
        hits_after = _load_contract_cached.cache_info().hits
        assert hits_after > hits_before, f"Cache did not hit: before={hits_before}, after={hits_after}"

        # 2. Modify contract on disk (change the schema completely) and update mtime using os.utime
        contract_2 = {"age": "number"}
        with open(contract_path, "w") as f:
            json.dump(contract_2, f)

        # Explicitly modify file's timestamp to prevent flakiness from rapid writes
        mtime = os.path.getmtime(contract_path)
        os.utime(contract_path, (mtime + 5.0, mtime + 5.0))

        # Now validate against the new contract schema
        # {"name": "test"} should now fail, {"age": 42} should succeed
        assert validate_contract({"name": "test"}, contract_path) is False
        assert validate_contract({"age": 42}, contract_path) is True

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
