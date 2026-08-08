import os
import json
import time
from utils.gem_core import validate_contract, _load_contract_cached


def test_validate_contract_cache_correctness():
    # 1. Create a temporary contract
    contract_path = "tests/temp_test_contract.json"
    initial_contract = {"id": "string", "value": "number"}
    with open(contract_path, "w") as f:
        json.dump(initial_contract, f)

    try:
        # Check validation succeeds
        data_valid = {"id": "123", "value": 45.6}
        assert validate_contract(data_valid, contract_path) is True

        # Check validation fails on bad type
        data_invalid = {"id": "123", "value": "not-a-number"}
        assert validate_contract(data_invalid, contract_path) is False

        # 2. Modify contract on disk (with new type expectation)
        modified_contract = {
            "id": "string",
            "value": "string",  # now expects a string
        }
        with open(contract_path, "w") as f:
            json.dump(modified_contract, f)

        # Explicitly update mtime to ensure filesystem registers modification
        # and doesn't suffer from filesystem time resolution limits
        os.utime(contract_path, (time.time() + 10, time.time() + 10))

        # Now, old valid (where value is float) should fail
        assert validate_contract(data_valid, contract_path) is False

        # New valid (where value is string) should succeed
        new_data_valid = {"id": "123", "value": "it-is-a-string-now"}
        assert validate_contract(new_data_valid, contract_path) is True

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)


def test_validate_contract_benchmark():
    # Run a quick performance benchmark comparison
    contract_path = "tests/temp_benchmark_contract.json"
    contract_data = {
        "field1": "string",
        "field2": "number",
        "field3": "boolean",
        "field4": "array",
        "field5": "object",
    }
    with open(contract_path, "w") as f:
        json.dump(contract_data, f)

    test_payload = {
        "field1": "hello",
        "field2": 123.45,
        "field3": True,
        "field4": [1, 2, 3],
        "field5": {"key": "val"},
    }

    try:
        # Warmup and clear cache if needed
        _load_contract_cached.cache_clear()

        # Benchmark with cache
        t0 = time.perf_counter()
        for _ in range(1000):
            validate_contract(test_payload, contract_path)
        t_cached = time.perf_counter() - t0

        # Benchmark without cache (simulate by clearing cache every loop)
        t1 = time.perf_counter()
        for _ in range(1000):
            _load_contract_cached.cache_clear()
            validate_contract(test_payload, contract_path)
        t_uncached = time.perf_counter() - t1

        print("\n--- Cache Optimization Benchmark (1,000 iterations) ---")
        print(f"Time with caching: {t_cached:.5f}s")
        print(f"Time without caching (forced disk reads): {t_uncached:.5f}s")
        speedup = t_uncached / t_cached if t_cached > 0 else 1.0
        print(f"Speedup: {speedup:.2f}x faster")
        assert speedup > 1.5, f"Expected speedup to be significant, got {speedup:.2f}x"

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
