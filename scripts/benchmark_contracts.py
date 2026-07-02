import time
import os
import sys

# Add current directory to path so we can import utils
sys.path.append(os.getcwd())

from utils.gem_core import validate_contract

def benchmark_validate_contract(iterations=1000):
    contract_path = "contracts/gem1_output.schema.json"
    data = {
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.95,
        "execution_metadata": {"time": 100}
    }

    # Warm up
    validate_contract(data, contract_path)

    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for validate_contract over {iterations} iterations: {avg_time:.6f} seconds")
    return avg_time

if __name__ == "__main__":
    benchmark_validate_contract()
