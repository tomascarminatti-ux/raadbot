import time
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "candidate_data": {"name": "John Doe", "experience": "10 years", "skills": ["Python", "AI"]},
        "search_inputs": {"role": "Senior Engineer", "company": "Tech Corp"},
        "context": "Some long context about the search and the candidate...",
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001"
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    try:
        benchmark()
    except Exception as e:
        print(f"Error during benchmark: {e}")
