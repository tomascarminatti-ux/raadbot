import time
import json
import os
from utils.gem_core import validate_contract

def run_benchmark():
    contract_path = "tests/benchmark_temp_contract.json"
    os.makedirs("tests", exist_ok=True)
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean"
    }
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    valid_data = {
        "name": "Benchmark Candidate",
        "score": 0.95,
        "is_active": True
    }

    iterations = 2000

    # Uncached run (simulating old behavior by reading file directly inside the loop)
    start_uncached = time.perf_counter()
    for _ in range(iterations):
        with open(contract_path, "r") as f:
            _ = json.load(f)
        # Dummy validation
        _ = isinstance(valid_data.get("name"), str) and isinstance(valid_data.get("score"), (int, float))
    duration_uncached = time.perf_counter() - start_uncached

    # Cached run (using the optimized validate_contract)
    # Prime the cache first
    validate_contract(valid_data, contract_path)

    start_cached = time.perf_counter()
    for _ in range(iterations):
        validate_contract(valid_data, contract_path)
    duration_cached = time.perf_counter() - start_cached

    print(f"--- Benchmark Results ({iterations} iterations) ---")
    print(f"Uncached execution time: {duration_uncached:.5f}s")
    print(f"Cached execution time: {duration_cached:.5f}s")
    speedup = duration_uncached / duration_cached
    print(f"Speedup: {speedup:.2f}x")

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)

if __name__ == "__main__":
    run_benchmark()
