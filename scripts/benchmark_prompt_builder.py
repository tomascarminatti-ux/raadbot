import time
import os
import sys

# Add root to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt():
    variables = {
        "search_id": "test_search",
        "candidate_id": "candidate_1",
        "context": {
            "search_inputs": {"key": "value" * 100},
            "candidate_data": {"name": "John Doe", "resume": "Experienced engineer..." * 100},
            "working_memory": [{"step": 1, "agent": "gem1", "thought": "Thinking..." * 10}] * 5
        }
    }

    # Pre-load to avoid first-time disk I/O distortion
    build_prompt("gem1", variables)

    start = time.perf_counter()
    n = 100
    for _ in range(n):
        build_prompt("gem1", variables)
    end = time.perf_counter()
    print(f"Average build_prompt time: {(end - start) / n:.6f}s")

if __name__ == "__main__":
    benchmark_build_prompt()
