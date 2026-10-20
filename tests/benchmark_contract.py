import json
import os
import time
from utils.gem_core import validate_contract, _load_contract_cached


def run_benchmark():
    contract_path = "tests/temp_benchmark_contract.json"
    os.makedirs("tests", exist_ok=True)
    contract = {
        "discovery_dataset": "array",
        "confidence_score": "number",
        "reasoning_summary": "string",
        "qa_score": "number",
        "human_required": "boolean",
    }
    with open(contract_path, "w", encoding="utf-8") as f:
        json.dump(contract, f)

    data = {
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.95,
        "reasoning_summary": "Meets criteria",
        "qa_score": 0.99,
        "human_required": False,
    }

    iterations = 20000

    # Benchmark uncached reading
    _load_contract_cached.cache_clear()
    start_time = time.perf_counter()
    for _ in range(iterations):
        _load_contract_cached.cache_clear()
        validate_contract(data, contract_path)
    uncached_duration = time.perf_counter() - start_time

    # Benchmark cached reading
    _load_contract_cached.cache_clear()
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    cached_duration = time.perf_counter() - start_time

    if os.path.exists(contract_path):
        os.remove(contract_path)

    speedup = uncached_duration / cached_duration if cached_duration > 0 else 0
    print(f"Iterations: {iterations}")
    print(f"Uncached Time: {uncached_duration * 1000:.2f} ms")
    print(f"Cached Time:   {cached_duration * 1000:.2f} ms")
    print(f"Speedup:       {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
