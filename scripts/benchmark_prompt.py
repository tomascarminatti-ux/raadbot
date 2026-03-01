import time
import json
import os
import sys

# Ensure we can import from the root
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    gem_name = "gem1"
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "context": {"some": "data", "more": "data"},
        "input": {"payload": "test"}
    }

    # Warm up
    for _ in range(10):
        build_prompt(gem_name, variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
