import time
import os
import json
from agent.prompt_builder import build_prompt
from utils.gem_core import validate_contract


def benchmark_prompt_builder(iterations=1000):
    variables = {
        "search_id": "test-search",
        "candidate_id": "cand-001",
        "context": {"key": "value", "nested": {"a": 1}}
    }

    start_time = time.time()
    for _ in range(iterations):
        build_prompt("gem6", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations * 1000
    msg = f"Prompt Builder: Avg time per call over {iterations} "
    msg += f"iterations: {avg_time:.4f} ms"
    print(msg)
    return avg_time


def benchmark_contract_validation(iterations=1000):
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean"
    }
    contract_path = "tests/benchmark_contract.json"
    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    data = {
        "name": "Test",
        "score": 0.9,
        "is_active": True
    }

    start_time = time.time()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations * 1000
    msg = f"Contract Validation: Avg time per call over {iterations} "
    msg += f"iterations: {avg_time:.4f} ms"
    print(msg)

    if os.path.exists(contract_path):
        os.remove(contract_path)
    return avg_time


if __name__ == "__main__":
    print("Starting Benchmark...")
    benchmark_prompt_builder()
    benchmark_contract_validation()
