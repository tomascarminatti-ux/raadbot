import os
import sys
import time

# Ensure project root is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gem_core import validate_contract
from agent.prompt_builder import build_prompt

def run_benchmark():
    print("=== PERFORMANCE BENCHMARK ===")

    # 1. Benchmark contract validation
    contract_path = "contracts/gem2_output.schema.json"
    data = {"score": 0.85}

    # Warm up
    validate_contract(data, contract_path)

    start_time = time.perf_counter()
    iterations = 2000
    for _ in range(iterations):
        validate_contract(data, contract_path)
    end_time = time.perf_counter()

    contract_duration = end_time - start_time
    avg_contract_time = (contract_duration / iterations) * 1000 # in ms
    print(f"Contract validation ({iterations} runs): {contract_duration:.4f} seconds total")
    print(f"Average contract validation time: {avg_contract_time:.6f} ms per call")

    # 2. Benchmark prompt building
    variables = {
        "input": {
            "role": "Staff Data Engineer",
            "location": "Madrid, Remoto España",
            "skills": "Python, Spark, AWS"
        }
    }

    # Warm up
    build_prompt("gem5", variables)

    start_time = time.perf_counter()
    prompt_iterations = 500
    for _ in range(prompt_iterations):
        build_prompt("gem5", variables)
    end_time = time.perf_counter()

    prompt_duration = end_time - start_time
    avg_prompt_time = (prompt_duration / prompt_iterations) * 1000 # in ms
    print(f"Prompt building ({prompt_iterations} runs): {prompt_duration:.4f} seconds total")
    print(f"Average prompt building time: {avg_prompt_time:.6f} ms per call")

if __name__ == "__main__":
    run_benchmark()
