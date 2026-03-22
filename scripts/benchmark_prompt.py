import time
import os
import sys
from unittest.mock import MagicMock

# Add current directory to path so we can import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=100):
    variables = {
        "search_id": "test_search",
        "candidate_id": "test_cand",
        "cv_text": "This is a long CV text " * 100,
        "interview_notes": "Good candidate " * 50,
        "gem5_summary": "Summary of search " * 20
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        # We use gem1 as it's a typical prompt
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Total time for {iterations} iterations: {total_time:.4f}s")
    print(f"Average time per call: {avg_time:.6f}s")
    return avg_time

if __name__ == "__main__":
    print("Running benchmark...")
    benchmark_build_prompt()
