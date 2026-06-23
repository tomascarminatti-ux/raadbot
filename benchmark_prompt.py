import time
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "test-search",
        "candidate_id": "cand-001",
        "context": "Some context information here"
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
