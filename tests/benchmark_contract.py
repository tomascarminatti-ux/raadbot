"""
Benchmark uncached vs cached contract schema loading in validate_contract.
"""

import json
import timeit
from typing import Dict, Any


def validate_contract_uncached(data: Dict[str, Any], path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
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
    from utils.gem_core import validate_contract

    contract_path = "contracts/gem1_output.schema.json"
    sample_data = {
        "discovery_dataset": ["cand_01", "cand_02"],
        "confidence_score": 0.95,
        "execution_metadata": {"source": "serp"},
    }

    iterations = 5000

    # Warmup
    validate_contract_uncached(sample_data, contract_path)
    validate_contract(sample_data, contract_path)

    t_uncached = timeit.timeit(
        lambda: validate_contract_uncached(sample_data, contract_path),
        number=iterations,
    )
    t_cached = timeit.timeit(
        lambda: validate_contract(sample_data, contract_path),
        number=iterations,
    )

    speedup = t_uncached / t_cached
    print(f"=== Contract Validation Benchmark ({iterations} iterations) ===")
    print(f"Uncached file I/O + parsing: {t_uncached:.4f}s")
    print(f"Cached schema loading:        {t_cached:.4f}s")
    print(f"Speedup:                      {speedup:.2f}x faster")
    print("=============================================================")


if __name__ == "__main__":
    run_benchmark()
