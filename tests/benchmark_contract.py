import time
import logging
from utils.gem_core import validate_contract, logger

# Suppress logging during benchmark
logger.setLevel(logging.ERROR)

def main():
    contract_path = "contracts/gem1_output.schema.json"
    valid_data = {
        "discovery_dataset": [{"id": 1}],
        "confidence_score": 0.9,
        "execution_metadata": {"time": 123}
    }

    iterations = 20000

    # Warmup
    validate_contract(valid_data, contract_path)

    start = time.perf_counter()
    for _ in range(iterations):
        validate_contract(valid_data, contract_path)
    elapsed = time.perf_counter() - start

    avg_time_ms = (elapsed * 1000) / iterations
    print(f"Contract validation benchmark ({iterations} calls):")
    print(f"  Total time: {elapsed:.4f} seconds")
    print(f"  Avg time per call: {avg_time_ms:.6f} ms")

if __name__ == "__main__":
    main()
