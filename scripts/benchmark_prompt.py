
import time
import os
import sys

# Ensure project root is in path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-candidate",
        "cv_text": "This is a long CV text " * 100,
        "interview_notes": "Some notes about the interview " * 50,
        "gem5_summary": "Summary of GEM5 " * 20,
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end = time.perf_counter()

    avg_time_ms = (end - start) / iterations * 1000
    print(f"Average time per build_prompt call: {avg_time_ms:.4f} ms")

if __name__ == "__main__":
    benchmark()
