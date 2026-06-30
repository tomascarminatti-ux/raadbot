import os
import sys
import time


def benchmark_build_prompt():
    # Add the root directory to sys.path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agent.prompt_builder import build_prompt

    variables = {
        "search_id": "test-search",
        "candidate_id": "candidate-123",
        "input": {"name": "John Doe", "experience": "10 years"},
        "context": {"company": "Tech Corp", "role": "Senior Engineer"}
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem5", variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem5", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations * 1000
    print(f"Average time for build_prompt: {avg_time:.4f} ms")


if __name__ == "__main__":
    benchmark_build_prompt()
