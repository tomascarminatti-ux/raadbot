import time
from utils.gem_core import validate_contract

def run_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    valid_data = {
        "discovery_dataset": [{"id": 1}],
        "confidence_score": 0.95,
        "execution_metadata": {"elapsed_time": 2.5}
    }

    # Warm up
    validate_contract(valid_data, contract_path)

    iterations = 1000
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(valid_data, contract_path)
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"Benchmark: {iterations} iterations took {elapsed:.5f} seconds.")
    print(f"Average time per call: {elapsed / iterations * 1000:.5f} ms")

if __name__ == "__main__":
    run_benchmark()
