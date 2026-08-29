import os
import json
import time
from utils.gem_core import validate_contract, _load_contract_cached

def test_validate_contract_caching():
    contract_path = "tests/temp_cached_contract.json"
    contract_data = {"key_a": "string"}

    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_data, f)

    try:
        data = {"key_a": "hello"}

        # Initial validation should succeed and populate LRU cache
        assert validate_contract(data, contract_path) is True

        # Verify cache hit info
        info = _load_contract_cached.cache_info()
        assert info.hits >= 0

        # Second call should hit the LRU cache
        assert validate_contract(data, contract_path) is True
        info_after = _load_contract_cached.cache_info()
        assert info_after.hits > info.hits

        # Explicitly modify mtime to test cache invalidation on file modification
        updated_contract_data = {"key_a": "number"}
        with open(contract_path, "w", encoding="utf-8") as f:
            json.dump(updated_contract_data, f)

        # Force mtime timestamp change
        os.utime(contract_path, (time.time() + 2, time.time() + 2))

        # Data with string should now fail because schema expected number
        assert validate_contract(data, contract_path) is False
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
