import json
import os
import time
from utils.gem_core import validate_contract, _load_contract_cached

def main():
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object"
    }
    contract_path = "tests/benchmark_contract.json"
    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    valid_data = {
        "name": "BenchmarkTest",
        "score": 42.0,
        "is_active": True,
        "tags": ["perf", "cache"],
        "metadata": {"env": "test"}
    }

    iterations = 1000

    # Benchmark cached validate_contract
    _load_contract_cached.cache_clear()
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(valid_data, contract_path)
    cached_duration = time.perf_counter() - start_time

    # Benchmark uncached reading (direct disk read + json load)
    start_time = time.perf_counter()
    for _ in range(iterations):
        with open(contract_path, "r") as f:
            c = json.load(f)
        for key, expected_type in c.items():
            val = valid_data.get(key)
    uncached_duration = time.perf_counter() - start_time

    speedup = uncached_duration / cached_duration if cached_duration > 0 else 0

    print(f"Iterations: {iterations}")
    print(f"Uncached duration: {uncached_duration:.5f} s")
    print(f"Cached duration:   {cached_duration:.5f} s")
    print(f"Speedup:           {speedup:.2f}x")

    if os.path.exists(contract_path):
        os.remove(contract_path)

if __name__ == "__main__":
    main()
