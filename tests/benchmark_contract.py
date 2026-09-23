import json
import os
import time
from utils.gem_core import _load_contract_cached, validate_contract

def run_benchmark():
    contract_path = "tests/temp_bench_contract.json"
    os.makedirs("tests", exist_ok=True)

    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object"
    }

    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract, f)

    data = {
        "name": "Candidate",
        "score": 0.95,
        "is_active": True,
        "tags": ["python", "ai"],
        "metadata": {"role": "senior"}
    }

    iterations = 1000

    # Benchmark without cache
    _load_contract_cached.cache_clear()
    t0 = time.perf_counter()
    for _ in range(iterations):
        # Read from disk directly to simulate un-cached performance
        with open(contract_path, "r", encoding="utf-8") as f:
            c = json.load(f)
        for key, expected_type in c.items():
            val = data.get(key)
            if expected_type == "string" and not isinstance(val, str):
                pass
    t1 = time.perf_counter()
    uncached_time = t1 - t0

    # Benchmark with cache
    _load_contract_cached.cache_clear()
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    t2 = time.perf_counter()
    cached_time = t2 - t0

    print(f"Uncached contract load time ({iterations} iterations): {uncached_time:.5f}s")
    print(f"Cached contract load time   ({iterations} iterations): {cached_time:.5f}s")
    if cached_time > 0:
        speedup = uncached_time / cached_time
        print(f"Speedup: {speedup:.2f}x faster")

    if os.path.exists(contract_path):
        os.remove(contract_path)

if __name__ == "__main__":
    run_benchmark()
