import time
from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "candidate_id": "CAND-001",
        "search_id": "SEARCH-001",
        "input": {"key": "value" * 100},
        "context": {"key": "value" * 100}
    }

    start_time = time.time()
    for _ in range(1000):
        build_prompt("gem1", variables)
    end_time = time.time()

    print(f"Time for 1000 build_prompt calls: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    benchmark()
