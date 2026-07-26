import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import load_prompt, build_prompt
from utils.gem_core import validate_contract

def run_benchmarks():
    print("--- Running Benchmarks (BEFORE Optimization) ---")

    # 1. Prompt Loading Benchmark
    start_time = time.perf_counter()
    iterations = 500
    for _ in range(iterations):
        _ = load_prompt("gem1")
    end_time = time.perf_counter()
    prompt_load_time = end_time - start_time
    print(f"load_prompt('gem1') x {iterations}: {prompt_load_time:.4f} seconds ({prompt_load_time/iterations*1000:.4f} ms per call)")

    # 2. Build Prompt Benchmark
    start_time = time.perf_counter()
    variables = {"input": {"name": "test", "score": 0.95}}
    for _ in range(iterations):
        _ = build_prompt("gem1", variables)
    end_time = time.perf_counter()
    build_prompt_time = end_time - start_time
    print(f"build_prompt('gem1') x {iterations}: {build_prompt_time:.4f} seconds ({build_prompt_time/iterations*1000:.4f} ms per call)")

    # 3. Contract Validation Benchmark
    # Create temp contract
    import json
    contract = {
        "discovery_dataset": "array",
        "confidence_score": "number",
        "execution_metadata": "object"
    }
    contract_path = "tests/temp_contract_bench.json"
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    valid_data = {
        "discovery_dataset": ["item1"],
        "confidence_score": 0.9,
        "execution_metadata": {}
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = validate_contract(valid_data, contract_path)
    end_time = time.perf_counter()
    contract_validation_time = end_time - start_time
    print(f"validate_contract x {iterations}: {contract_validation_time:.4f} seconds ({contract_validation_time/iterations*1000:.4f} ms per call)")

    if os.path.exists(contract_path):
        os.remove(contract_path)

if __name__ == "__main__":
    run_benchmarks()
