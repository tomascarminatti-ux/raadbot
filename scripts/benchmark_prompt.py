import time
import sys
import os
import json

# Add parent directory to sys.path to import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "context": {
            "key1": "value1",
            "key2": "value2",
            "key3": ["item1", "item2"]
        },
        "input": "Some test input"
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    try:
        benchmark()
    except Exception as e:
        print(f"Error during benchmark: {e}")
