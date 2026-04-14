
import time
import os
import sys

# Add the project root to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    gem_name = "gem1"
    variables = {
        "search_id": "test_search",
        "candidate_id": "test_cand",
        "cv_text": "This is a long CV text " * 100,
        "interview_notes": "Good candidate " * 50,
        "gem5_summary": "Summary of search " * 20
    }

    # Warm up
    build_prompt(gem_name, variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time to build prompt (1000 iterations): {avg_time:.6f} seconds")

if __name__ == "__main__":
    benchmark()
