import time
import os
import sys

# Ensure PYTHONPATH includes repo root
sys.path.append(os.getcwd())

from utils.gem_core import validate_contract
from agent.prompt_builder import build_prompt

def run_benchmark():
    print("--- Running Performance Benchmark ---")

    # 1. Benchmark contract validation
    sample_data = {"score": 0.85}
    contract_path = "contracts/gem2_output.schema.json"

    start_time = time.perf_counter()
    iterations = 2000
    for _ in range(iterations):
        validate_contract(sample_data, contract_path)
    contract_duration = time.perf_counter() - start_time
    print(f"Contract Validation ({iterations} iterations): {contract_duration:.4f} seconds ({contract_duration/iterations * 1000:.6f} ms per call)")

    # 2. Benchmark prompt building
    sample_variables = {
        "input": {
            "role": "Staff Data Engineer",
            "location": "Madrid",
            "skills": "Python, Spark"
        }
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem5", sample_variables)
    prompt_duration = time.perf_counter() - start_time
    print(f"Prompt Building ({iterations} iterations): {prompt_duration:.4f} seconds ({prompt_duration/iterations * 1000:.6f} ms per call)")

if __name__ == "__main__":
    run_benchmark()
