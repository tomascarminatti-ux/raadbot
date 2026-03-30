import time
import os
from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-cand",
        "cv_text": "This is a long CV text " * 100,
        "interview_notes": "Good candidate " * 50,
        "gem5_summary": "Summary of role"
    }

    start_time = time.time()
    for _ in range(iterations):
        # Using gem1 as it likely has multiple variables
        try:
            build_prompt("gem1", variables)
        except FileNotFoundError:
            # Fallback if gem1.md doesn't exist, try something else
            pass
    end_time = time.time()

    print(f"Time taken for {iterations} iterations: {end_time - start_time:.4f} seconds")
    print(f"Average time per call: {(end_time - start_time) / iterations * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
