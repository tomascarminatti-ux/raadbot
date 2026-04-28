import time
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-001",
        "cv_text": "This is a very long CV text " * 100,
        "interview_notes": "Great candidate " * 50,
        "gem5_summary": "Summary of GEM5 " * 20
    }

    iterations = 100
    start_time = time.time()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time:.6f} seconds")

if __name__ == "__main__":
    benchmark()
