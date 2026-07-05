import time
import os
import sys

# Add the current directory to sys.path to import agent modules
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    variables = {
        "search_id": "test_search",
        "candidate_id": "test_cand",
        "cv_text": "This is a sample CV text for benchmarking purposes.",
        "interview_notes": "The candidate performed well in the interview.",
        "gem5_summary": "Summary of GEM5 analysis."
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        # Using gem1 as an example as it uses several variables
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Benchmark: build_prompt over {iterations} iterations")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time: {avg_time:.6f} seconds")

if __name__ == "__main__":
    benchmark_build_prompt()
