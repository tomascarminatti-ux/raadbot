
import time
from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    variables = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "context": {
            "some_key": "some_value",
            "another_key": 123
        }
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Benchmark results over {iterations} iterations:")
    print(f"Total time: {total_time:.4f} seconds")
    print(f"Average time per build_prompt: {avg_time * 1000:.4f} ms")

if __name__ == "__main__":
    # Warm up
    build_prompt("gem1", {"search_id": "test", "candidate_id": "test", "context": {}})
    benchmark_build_prompt()
