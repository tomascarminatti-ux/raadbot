"""
benchmark_contract.py - Compares contract validation speed with and without LRU caching.
"""

import time
import os
import json
from typing import Dict, Any
from utils.gem_core import validate_contract, _load_contract_cached


def validate_contract_uncached(data: Dict[str, Any], contract_path: str) -> bool:
    try:
        with open(contract_path, "r") as f:
            contract = json.load(f)

        for key in contract:
            if not isinstance(key, str):
                continue
            expected_type = contract[key]
            if key not in data:
                return False
            val = data.get(key)
            if expected_type == "array" and not isinstance(val, list):
                return False
            if expected_type == "number" and not isinstance(val, (int, float)):
                return False
            if expected_type == "string" and not isinstance(val, str):
                return False
            if expected_type == "object" and not isinstance(val, dict):
                return False
            if expected_type == "boolean" and not isinstance(val, bool):
                return False

        return True
    except Exception:
        return False


def run_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    if not os.path.exists(contract_path):
        print(f"Contract file {contract_path} not found.")
        return

    data = {
        "discovery_dataset": ["candidate_1"],
        "confidence_score": 0.95,
        "execution_metadata": {"time": 100}
    }

    iterations = 10000

    start = time.perf_counter()
    for _ in range(iterations):
        validate_contract_uncached(data, contract_path)
    uncached_time = time.perf_counter() - start

    _load_contract_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    cached_time = time.perf_counter() - start

    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print(f"--- Contract Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached execution time: {uncached_time:.5f}s")
    print(f"Cached execution time:   {cached_time:.5f}s")
    print(f"Speedup achieved:        {speedup:.2f}x faster")


if __name__ == "__main__":
    run_benchmark()
