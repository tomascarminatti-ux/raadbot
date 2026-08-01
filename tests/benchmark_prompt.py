import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

def run_benchmark():
    variables = {
        "search_id": "TEST-123",
        "candidate_id": "CAND-001",
        "context": "Some test context with experience, skills, and background."
    }

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        _ = build_prompt("gem6", variables)
    end_time = time.perf_counter()

    total_time_ms = (end_time - start_time) * 1000
    avg_time_ms = total_time_ms / iterations
    print(f"Iterations: {iterations}")
    print(f"Total time: {total_time_ms:.2f} ms")
    print(f"Average time per call: {avg_time_ms:.4f} ms")

if __name__ == "__main__":
    run_benchmark()
