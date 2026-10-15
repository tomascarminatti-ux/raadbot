import os
import json
import time
from utils.gem_core import validate_contract, _load_contract_cached

def validate_contract_uncached(data: dict, contract_path: str) -> bool:
    try:
        with open(contract_path, "r", encoding="utf-8") as f:
            contract = json.load(f)
        for key in contract:
            if not isinstance(key, str):
                continue
            expected_type = contract[key]
            if key not in data:
                return False
            val = data.get(key)
            if expected_type == "array" and not isinstance(val, list): return False
            if expected_type == "number" and not isinstance(val, (int, float)): return False
            if expected_type == "string" and not isinstance(val, str): return False
            if expected_type == "object" and not isinstance(val, dict): return False
            if expected_type == "boolean" and not isinstance(val, bool): return False
        return True
    except Exception:
        return False

def benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    if not os.path.exists(contract_path):
        print(f"Contract file not found at {contract_path}")
        return

    sample_data = {
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.92,
        "execution_metadata": {"time": 100}
    }

    N = 10000

    # Warmup
    validate_contract_uncached(sample_data, contract_path)
    validate_contract(sample_data, contract_path)

    # Measure uncached
    start = time.perf_counter()
    for _ in range(N):
        validate_contract_uncached(sample_data, contract_path)
    dur_uncached = time.perf_counter() - start

    # Measure cached
    start = time.perf_counter()
    for _ in range(N):
        validate_contract(sample_data, contract_path)
    dur_cached = time.perf_counter() - start

    speedup = dur_uncached / dur_cached if dur_cached > 0 else 0.0

    print("=== Contract Validation Caching Benchmark ===")
    print(f"Iterations: {N}")
    print(f"Uncached Time: {dur_uncached:.4f}s ({dur_uncached / N * 1000:.4f} ms/call)")
    print(f"Cached Time:   {dur_cached:.4f}s ({dur_cached / N * 1000:.4f} ms/call)")
    print(f"Speedup:       {speedup:.2f}x")

if __name__ == "__main__":
    benchmark()
