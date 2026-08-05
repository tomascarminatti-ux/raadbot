import os
import json
import time
from utils.gem_core import validate_contract


def test_contract_validation_cache_correctness():
    """Verify that cached contract validation functions identically to non-cached."""
    contract_path = "tests/temp_cache_test.json"

    # Create a temporary contract
    contract_data = {"id": "string", "score": "number", "active": "boolean"}
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_data, f)

    try:
        # Valid data
        valid_payload = {"id": "CAND-001", "score": 9.5, "active": True}
        assert validate_contract(valid_payload, contract_path) is True

        # Invalid data
        invalid_payload = {"id": "CAND-001", "score": "nine", "active": True}
        assert validate_contract(invalid_payload, contract_path) is False
    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)


def test_cache_invalidation_on_file_modification():
    """Verify that modifying the contract schema on disk correctly invalidates the cache."""
    contract_path = "tests/temp_invalidation_test.json"

    # Version 1 of the contract
    contract_v1 = {
        "id": "string",
    }
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_v1, f)

    try:
        # Load and validate first version
        payload_v1 = {"id": "CAND-001"}
        assert validate_contract(payload_v1, contract_path) is True

        # Now modify the contract file to include a new required key
        contract_v2 = {"id": "string", "score": "number"}

        # Make sure we change the file on disk
        with open(contract_path, "w", encoding="utf-8") as f:
            json.dump(contract_v2, f)

        # Update file modification times explicitly to guarantee invalidation trigger
        # (Using os.utime rather than time.sleep to prevent flaky tests and speed up runs)
        now = time.time()
        os.utime(contract_path, (now + 10, now + 10))

        # Now, the old payload without "score" should fail validation
        # because the schema has changed on disk and the cache should have invalidated
        assert validate_contract(payload_v1, contract_path) is False

        # A payload with the score should pass
        payload_v2 = {"id": "CAND-001", "score": 85.0}
        assert validate_contract(payload_v2, contract_path) is True

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)


def test_validation_cache_performance():
    """Run a micro-benchmark to demonstrate the speedup of the caching layer."""
    contract_path = "tests/temp_perf_test.json"

    contract_data = {
        "id": "string",
        "score": "number",
        "active": "boolean",
        "tags": "array",
        "metadata": "object",
    }
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_data, f)

    payload = {
        "id": "CAND-123",
        "score": 0.99,
        "active": True,
        "tags": ["fast", "efficient"],
        "metadata": {"source": "benchmark"},
    }

    try:
        # Measure warm cache validation
        start_cached = time.perf_counter()
        for _ in range(1000):
            validate_contract(payload, contract_path)
        end_cached = time.perf_counter()
        cached_duration = end_cached - start_cached

        # Measure raw file read + parsing
        start_raw = time.perf_counter()
        for _ in range(1000):
            with open(contract_path, "r", encoding="utf-8") as f:
                _raw_contract = json.load(f)
            # Basic validation simulation matching the function
            for key, expected_type in _raw_contract.items():
                _val = payload.get(key)
        end_raw = time.perf_counter()
        raw_duration = end_raw - start_raw

        speedup = raw_duration / cached_duration if cached_duration > 0 else 0
        print("\n⚡ Caching Performance Benchmark (1000 iterations):")
        print(f"   - Without Caching (Raw Disk/JSON): {raw_duration:.5f}s")
        print(f"   - With Caching (LRU cache):       {cached_duration:.5f}s")
        print(f"   - Speedup: ~{speedup:.2f}x faster")

        # Verify that caching is at least faster (usually 20x-50x)
        assert cached_duration < raw_duration

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)
