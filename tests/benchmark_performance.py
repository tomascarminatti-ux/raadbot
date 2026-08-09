import time
import os
import json
from utils.gem_core import validate_contract

def run_benchmark():
    # Setup a temp contract and some test data
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object"
    }
    contract_path = "tests/benchmark_temp_contract.json"
    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    valid_data = {
        "name": "Benchmark Test",
        "score": 42.0,
        "is_active": True,
        "tags": ["performance", "speed"],
        "metadata": {"nested": "value"}
    }

    # Warm up
    validate_contract(valid_data, contract_path)

    iterations = 2000
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(valid_data, contract_path)
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"Iterations: {iterations}")
    print(f"Total time: {elapsed:.5f} seconds")
    print(f"Time per iteration: {(elapsed / iterations) * 1000_000:.3f} microseconds")

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)

if __name__ == "__main__":
    run_benchmark()
