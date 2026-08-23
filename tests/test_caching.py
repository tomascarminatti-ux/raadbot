import json
import os
import time
from utils.gem_core import validate_contract, _load_contract_cached


def test_contract_caching_correctness_and_invalidation():
    contract_path = "tests/temp_test_cache_contract.json"
    os.makedirs("tests", exist_ok=True)

    contract_v1 = {"field_a": "string"}
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract_v1, f)

    try:
        # Initial validation check
        data_v1 = {"field_a": "hello"}
        assert validate_contract(data_v1, contract_path) is True

        # Check cache hits
        hits_before = _load_contract_cached.cache_info().hits
        assert validate_contract(data_v1, contract_path) is True
        hits_after = _load_contract_cached.cache_info().hits
        assert hits_after > hits_before

        # Modify file on disk and explicitly update mtime
        contract_v2 = {"field_a": "string", "field_b": "number"}
        with open(contract_path, "w", encoding="utf-8") as f:
            json.dump(contract_v2, f)

        # Force new mtime using utime to ensure invalidation even on coarse filesystems
        st = os.stat(contract_path)
        os.utime(contract_path, (st.st_atime, st.st_mtime + 2.0))

        # Old data (missing field_b) should now fail validation
        assert validate_contract(data_v1, contract_path) is False

        # New data should pass
        data_v2 = {"field_a": "hello", "field_b": 42}
        assert validate_contract(data_v2, contract_path) is True

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)


def test_contract_validation_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    data = {
        "discovery_dataset": ["item1"],
        "confidence_score": 0.9,
        "execution_metadata": {},
    }

    start = time.perf_counter()
    for _ in range(1000):
        validate_contract(data, contract_path)
    elapsed = time.perf_counter() - start

    # Execution time for 1,000 cached contract validations should be under 0.05 seconds
    assert elapsed < 0.05, f"Expected <0.05s, got {elapsed:.4f}s"
