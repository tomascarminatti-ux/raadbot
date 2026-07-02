import time
import os
import sys

# Add current directory to path so we can import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=100):
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-candidate",
        "context": {
            "key1": "value1",
            "key2": "value2",
            "nested": {"a": 1, "b": 2}
        }
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt over {iterations} iterations: {avg_time:.6f} seconds")
    return avg_time

if __name__ == "__main__":
    # Ensure prompts exist for test
    os.makedirs("prompts", exist_ok=True)
    if not os.path.exists("prompts/00_prompt_maestro.md"):
        with open("prompts/00_prompt_maestro.md", "w") as f:
            f.write("Maestro prompt content with {{VERSION}}")
    if not os.path.exists("prompts/gem1.md"):
        with open("prompts/gem1.md", "w") as f:
            f.write("GEM1 prompt content with {{PROMPT_MAESTRO}}, {{search_id}}, and {{context}}")

    benchmark_build_prompt()
