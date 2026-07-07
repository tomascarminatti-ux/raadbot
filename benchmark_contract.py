import time
import os
import sys

# Add the current directory to sys.path to import agent
sys.path.append(os.getcwd())

from utils.gem_core import validate_contract

def benchmark_validate_contract(iterations=1000):
    data = {
        "score": 0.85,
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.9,
        "decision": "ACCEPT",
        "qa_score": 0.98
    }

    os.makedirs("contracts", exist_ok=True)
    contract_path = "contracts/test_contract.json"
    with open(contract_path, "w") as f:
        import json
        json.dump({
            "score": "number",
            "discovery_dataset": "array",
            "confidence_score": "number",
            "decision": "string",
            "qa_score": "number"
        }, f)

    start_time = time.time()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per validate_contract: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_validate_contract()
