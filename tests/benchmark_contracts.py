import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.gem_core import validate_contract

def run_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    data = {
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.85,
        "execution_metadata": {"time": "12s"}
    }

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        _ = validate_contract(data, contract_path)
    end_time = time.perf_counter()

    total_time_ms = (end_time - start_time) * 1000
    avg_time_ms = total_time_ms / iterations
    print(f"Iterations: {iterations}")
    print(f"Total time: {total_time_ms:.2f} ms")
    print(f"Average time per call: {avg_time_ms:.4f} ms")

if __name__ == "__main__":
    run_benchmark()
