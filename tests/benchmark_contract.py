import os
import json
import time
from utils.gem_core import validate_contract, _load_contract_cached

def benchmark():
    contract_path = "tests/temp_benchmark_contract.json"
    contract = {
        "candidate_id": "string",
        "score": "number",
        "recommended": "boolean",
        "notes": "string"
    }

    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    data = {
        "candidate_id": "cand_123",
        "score": 92.5,
        "recommended": True,
        "notes": "Strong background in backend engineering"
    }

    iterations = 1000

    # Benchmark uncached disk load
    t0 = time.perf_counter()
    for _ in range(iterations):
        _load_contract_cached.cache_clear()
        validate_contract(data, contract_path)
    t1 = time.perf_counter()
    uncached_time = t1 - t0

    # Benchmark cached load
    _load_contract_cached.cache_clear()
    validate_contract(data, contract_path)  # Warmup
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    t1 = time.perf_counter()
    cached_time = t1 - t0

    speedup = uncached_time / cached_time if cached_time > 0 else 0
    print(f"Uncached contract validations ({iterations} iterations): {uncached_time:.5f}s")
    print(f"Cached contract validations ({iterations} iterations):   {cached_time:.5f}s")
    print(f"Speedup: {speedup:.2f}x faster")

    if os.path.exists(contract_path):
        os.remove(contract_path)

if __name__ == "__main__":
    benchmark()
