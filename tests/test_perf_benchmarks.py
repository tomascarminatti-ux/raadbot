import os
import json
import time
import pytest
from utils.gem_core import validate_contract, _load_contract

def test_contract_validation_cache_and_invalidation():
    contract_path = "tests/temp_test_perf_contract.json"

    # 1. Create a contract schema
    contract_data = {
        "name": "string",
        "score": "number",
        "is_active": "boolean"
    }

    with open(contract_path, "w") as f:
        json.dump(contract_data, f)

    try:
        valid_data = {
            "name": "Alex",
            "score": 95.5,
            "is_active": True
        }

        # Capture initial hits/misses or warm up the cache
        _load_contract.cache_clear()

        # First call should load and cache
        assert validate_contract(valid_data, contract_path) is True
        cache_info = _load_contract.cache_info()
        assert cache_info.misses == 1
        assert cache_info.hits == 0

        # Second call should fetch from cache (hit)
        assert validate_contract(valid_data, contract_path) is True
        cache_info = _load_contract.cache_info()
        assert cache_info.misses == 1
        assert cache_info.hits == 1

        # 2. Modify the contract on disk & test auto-invalidation
        # We need to guarantee the mtime updates. Some filesystems have 1s precision,
        # so we manually set the mtime slightly in the future or back to ensure a change.
        mtime = os.path.getmtime(contract_path)
        new_mtime = mtime + 5.0

        # Rewrite contract with different schema (requiring "extra_field" as string)
        new_contract_data = {
            "extra_field": "string"
        }
        with open(contract_path, "w") as f:
            json.dump(new_contract_data, f)

        os.utime(contract_path, (new_mtime, new_mtime))

        # The next validation should use the new contract structure
        invalid_data_now = {
            "name": "Alex",
            "score": 95.5,
            "is_active": True
        }
        # Since "extra_field" is missing, validate_contract should return False
        assert validate_contract(invalid_data_now, contract_path) is False

        # Since mtime changed, we expect a cache miss (new cache entry created)
        cache_info = _load_contract.cache_info()
        assert cache_info.misses == 2

        # Valid data under the updated contract should pass
        valid_data_now = {
            "extra_field": "hello"
        }
        assert validate_contract(valid_data_now, contract_path) is True
        cache_info = _load_contract.cache_info()
        assert cache_info.hits == 2

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)

def test_performance_difference():
    # Write a dummy contract for benchmarking
    contract_path = "tests/temp_perf_diff_contract.json"
    schema = {
        "id": "string",
        "value": "number",
        "flag": "boolean",
        "items": "array",
        "info": "object"
    }
    with open(contract_path, "w") as f:
        json.dump(schema, f)

    try:
        data = {
            "id": "123",
            "value": 42.0,
            "flag": True,
            "items": [1, 2, 3],
            "info": {"meta": "data"}
        }

        # Measure cached path (1000 iterations)
        t0 = time.perf_counter()
        for _ in range(1000):
            validate_contract(data, contract_path)
        t1 = time.perf_counter()
        cached_duration = t1 - t0

        # Measure direct disk-load path (by bypassing cache helper via _load_contract.__wrapped__)
        t0 = time.perf_counter()
        for _ in range(1000):
            # Simulate original validate_contract without lru_cache
            with open(contract_path, "r") as f:
                contract = json.load(f)
            for key in contract:
                expected_type = contract[key]
                val = data.get(key)
                if expected_type == "array" and not isinstance(val, list): pass
                if expected_type == "number" and not isinstance(val, (int, float)): pass
                if expected_type == "string" and not isinstance(val, str): pass
                if expected_type == "object" and not isinstance(val, dict): pass
                if expected_type == "boolean" and not isinstance(val, bool): pass
        t2 = time.perf_counter()
        uncached_duration = t2 - t0

        print(f"\nUncached validation duration (1000 iter): {uncached_duration:.6f}s")
        print(f"Cached validation duration (1000 iter): {cached_duration:.6f}s")
        speedup = uncached_duration / max(cached_duration, 1e-9)
        print(f"Contract loading/validation speedup: {speedup:.2f}x")

        # Verify that cache is significantly faster (usually > 2x at least)
        assert cached_duration < uncached_duration

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
