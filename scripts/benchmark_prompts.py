import time
import sys
import os

# Add the current directory to sys.path to import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_prompt_builder(iterations=100):
    variables = {
        "role": "Software Engineer",
        "location": "Madrid",
        "skills": "Python, FastAPI, Docker",
        "candidate_id": "CAND-001",
        "search_id": "SEARCH-001",
        "context": {"key": "value", "more": "data"}
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        # We use gem5 as an example
        build_prompt("gem5", variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Total time for {iterations} iterations: {total_time:.4f}s")
    print(f"Average time per prompt: {avg_time*1000:.4f}ms")

if __name__ == "__main__":
    try:
        benchmark_prompt_builder()
    except Exception as e:
        print(f"Error: {e}")
