import time
import re
import json
import os
import sys

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

def benchmark():
    gem_name = "gem1"
    # More variables to simulate real-world usage
    variables = {
        "candidate_id": "CAND-001",
        "search_id": "SEARCH-2026",
        "cv_text": "A very long CV " * 2000,
        "interview_notes": "Interesting interview " * 2000,
        "gem5_summary": "Detailed context " * 1000,
        "extra_1": "data" * 100,
        "extra_2": "data" * 100,
        "extra_3": "data" * 100,
        "extra_4": "data" * 100,
        "extra_5": "data" * 100,
    }

    # Warm up
    build_prompt(gem_name, variables)

    iterations = 200
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end = time.perf_counter()

    print(f"Current implementation: {end - start:.4f} seconds for {iterations} iterations")
    print(f"Average: {(end - start) / iterations * 1000:.4f} ms per iteration")

if __name__ == "__main__":
    benchmark()
