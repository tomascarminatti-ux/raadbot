import time
import os
import sys
sys.path.append(os.getcwd())
from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "TEST-123",
        "candidate_id": "CAND-456",
        "context": {
            "search_inputs": {"role": "Software Engineer", "company": "TechCorp"},
            "candidate_data": {"name": "John Doe", "experience": "5 years"},
            "working_memory": [
                {"step": 1, "agent": "gem1", "thought": "Analyzing experience", "observation": "Good match", "valid_contract": True}
            ]
        }
    }

    # Pre-warm
    build_prompt("gem6", variables)

    start = time.perf_counter()
    n = 1000
    for _ in range(n):
        build_prompt("gem6", variables)
    end = time.perf_counter()

    avg_time = (end - start) / n * 1000
    print(f"Average build_prompt time: {avg_time:.4f} ms")

if __name__ == "__main__":
    benchmark()
