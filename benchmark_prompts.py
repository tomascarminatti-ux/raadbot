
import time
import os
import sys

# Ensure we can import from the agent directory
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_prompt_builder(iterations=1000):
    variables = {
        "search_id": "test_search",
        "candidate_id": "test_cand",
        "cv_text": "Experienced software engineer with a focus on performance.",
        "interview_notes": "Very strong candidate, fits well with the team.",
        "gem5_summary": "Role requires high performance and security focus."
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = (total_time / iterations) * 1000  # in ms

    print(f"Total time for {iterations} iterations: {total_time:.4f} seconds")
    print(f"Average time per call: {avg_time:.4f} ms")

if __name__ == "__main__":
    benchmark_prompt_builder()
