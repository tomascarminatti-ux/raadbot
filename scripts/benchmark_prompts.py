
import time
import os
import sys
import json
import asyncio

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=100):
    variables = {
        "search_id": "TEST-SEARCH",
        "candidate_id": "CANDIDATE-001",
        "context": {
            "search_inputs": {"job": "Engineer"},
            "candidate_data": {"name": "John Doe"},
            "working_memory": []
        }
    }

    # Pre-warm
    build_prompt("gem6", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem6", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average build_prompt time: {avg_time*1000:.4f} ms")
    return avg_time

if __name__ == "__main__":
    benchmark_build_prompt()
