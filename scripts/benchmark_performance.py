
import time
import os
import sys
import json
import tempfile

# Add current directory to path so we can import agent and utils
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt
from utils.gem_core import validate_contract

def benchmark_prompt_builder(iterations=1000):
    start_time = time.time()
    for _ in range(iterations):
        # Using gem5 as it's a common one
        build_prompt("gem5", {"input": "test input"})
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time:.6f}s ({iterations} iterations)")
    return avg_time

def benchmark_validate_contract(iterations=1000):
    # Use a temporary file for benchmarking to avoid overwriting production schemas
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump({"test_key": "string"}, tmp)
        tmp_path = tmp.name

    try:
        data = {"test_key": "test value"}

        # Warm up cache
        validate_contract(data, tmp_path)

        start_time = time.time()
        for _ in range(iterations):
            validate_contract(data, tmp_path)
        end_time = time.time()
        avg_time = (end_time - start_time) / iterations
        print(f"Average time for validate_contract: {avg_time:.6f}s ({iterations} iterations)")
        return avg_time
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    print("Starting benchmarks...")
    benchmark_prompt_builder()
    benchmark_validate_contract()
