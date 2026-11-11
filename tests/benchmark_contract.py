"""
benchmark_contract.py – Benchmarks schema loading in validate_contract.
Compares uncached file reads against cached in-memory LRU loading.
"""

import json
import timeit

from utils.gem_core import validate_contract


def validate_contract_uncached(data: dict, contract_path: str) -> bool:
    try:
        with open(contract_path, "r", encoding="utf-8") as f:
            contract = json.load(f)

        for key, expected_type in contract.items():
            if not isinstance(key, str):
                continue
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
    sample_data = {
        "discovery_dataset": ["candidate_1", "candidate_2"],
        "confidence_score": 0.95,
        "execution_metadata": {"model": "gemini-1.5-pro", "version": "v1.2"},
    }
    contract_path = "contracts/gem1_output.schema.json"
    iterations = 20000

    print("Running Contract Validation Benchmark...")
    print(f"Contract: {contract_path} | Iterations: {iterations:,}")

    t_uncached = timeit.timeit(
        lambda: validate_contract_uncached(sample_data, contract_path),
        number=iterations,
    )
    t_cached = timeit.timeit(
        lambda: validate_contract(sample_data, contract_path),
        number=iterations,
    )

    ops_uncached = iterations / t_uncached
    ops_cached = iterations / t_cached
    speedup = t_uncached / t_cached

    print(f"Uncached: {t_uncached:.4f}s ({ops_uncached:,.0f} ops/sec)")
    print(f"Cached:   {t_cached:.4f}s ({ops_cached:,.0f} ops/sec)")
    print(f"Speedup:  {speedup:.2f}x faster")


if __name__ == "__main__":
    run_benchmark()
