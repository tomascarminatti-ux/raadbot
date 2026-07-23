import time
import os
import sys

# Ensure project root is in path
sys.path.append(os.getcwd())

from utils.gem_core import validate_contract
from agent.prompt_builder import build_prompt

def benchmark_contract_validation():
    print("--- Benchmarking Contract Validation ---")
    data = {
        "decision": "ACCEPT",
        "decision_confidence": 0.95,
        "reasoning_summary": "Meets all criteria"
    }
    contract_path = "contracts/gem3_output.schema.json"

    # Run once to warm up (if there is caching)
    validate_contract(data, contract_path)

    start_time = time.perf_counter()
    iterations = 2000
    for _ in range(iterations):
        validate_contract(data, contract_path)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time_ms = (total_time / iterations) * 1000
    print(f"Total time for {iterations} validations: {total_time:.4f} seconds")
    print(f"Average time per validation: {avg_time_ms:.6f} ms")
    return avg_time_ms

def benchmark_prompt_building():
    print("--- Benchmarking Prompt Building ---")
    variables = {
        "search_id": "TEST-SEARCH-100",
        "candidate_id": "CAND-001",
        "context": {
            "search_inputs": {"role": "Engineer"},
            "candidate_data": {"name": "Alice"},
            "working_memory": []
        }
    }

    # Run once to warm up (if there is caching)
    build_prompt("gem6", variables)

    start_time = time.perf_counter()
    iterations = 500
    for _ in range(iterations):
        build_prompt("gem6", variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time_ms = (total_time / iterations) * 1000
    print(f"Total time for {iterations} prompt constructions: {total_time:.4f} seconds")
    print(f"Average time per prompt construction: {avg_time_ms:.6f} ms")
    return avg_time_ms

if __name__ == "__main__":
    benchmark_contract_validation()
    print()
    benchmark_prompt_building()
