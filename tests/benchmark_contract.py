import time
import os
from utils.gem_core import validate_contract

def run_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    data = {
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.95,
        "execution_metadata": {"time": 100}
    }

    # Warmup
    validate_contract(data, contract_path)

    iterations = 20000
    start = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    elapsed = time.perf_counter() - start

    print(f"Validated contract {iterations} times in {elapsed:.4f}s ({iterations/elapsed:.2f} ops/sec)")

if __name__ == "__main__":
    run_benchmark()
