import time
from agent.prompt_builder import load_prompt

def run_benchmark():
    iterations = 1000
    # Warm up
    load_prompt("gem1")

    start_time = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem1")
    end_time = time.perf_counter()

    elapsed = end_time - start_time
    print(f"Benchmark: {iterations} iterations took {elapsed:.5f} seconds.")
    print(f"Average time per call: {elapsed / iterations * 1000:.5f} ms")

if __name__ == "__main__":
    run_benchmark()
