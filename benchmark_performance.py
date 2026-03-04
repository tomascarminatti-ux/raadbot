import time
import os
import sys
import json
import functools

# Add current directory to path
sys.path.append(os.getcwd())

from agent.prompt_builder import load_prompt, build_prompt
from utils.gem_core import validate_contract

def benchmark(func, *args, iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        func(*args)
    end = time.perf_counter()
    return (end - start) * 1000 / iterations

def run_benchmarks(label="BASELINE"):
    print(f"\n--- Benchmarking {label} ---")

    # Benchmark load_prompt
    try:
        avg_load = benchmark(load_prompt, "gem1")
        print(f"load_prompt('gem1'): {avg_load:.4f} ms/op")
    except Exception as e:
        print(f"Error benchmarking load_prompt: {e}")

    # Benchmark build_prompt
    try:
        variables = {"input": {"test": "data"}}
        avg_build = benchmark(build_prompt, "gem1", variables)
        print(f"build_prompt('gem1'): {avg_build:.4f} ms/op")
    except Exception as e:
        print(f"Error benchmarking build_prompt: {e}")

    # Benchmark validate_contract
    try:
        contract_path = "contracts/gem1_output.schema.json"
        data = {
            "discovery_dataset": ["item1"],
            "confidence_score": 0.9,
            "execution_metadata": {}
        }
        avg_validate = benchmark(validate_contract, data, contract_path)
        print(f"validate_contract('gem1'): {avg_validate:.4f} ms/op")
    except Exception as e:
        print(f"Error benchmarking validate_contract: {e}")

if __name__ == "__main__":
    run_benchmarks()
