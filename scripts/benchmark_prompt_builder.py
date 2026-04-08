
import time
import os
import sys

# Add the current directory to sys.path to import agent modules
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    gem_name = "gem1"
    # Create a dummy prompt file for testing if it doesn't exist
    prompts_dir = os.path.join("prompts")
    os.makedirs(prompts_dir, exist_ok=True)

    maestro_path = os.path.join(prompts_dir, "00_prompt_maestro.md")
    if not os.path.exists(maestro_path):
        with open(maestro_path, "w") as f:
            f.write("This is the maestro prompt. VERSION: {{VERSION}}")

    gem_path = os.path.join(prompts_dir, "gem1.md")
    if not os.path.exists(gem_path):
        with open(gem_path, "w") as f:
            f.write("{{PROMPT_MAESTRO}}\nGEM1: {{var1}} and {{var2}}")

    variables = {
        "var1": "value1",
        "var2": {"nested": "value2"},
        "search_id": "test_search",
        "candidate_id": "test_cand"
    }

    # Warm up
    for _ in range(10):
        build_prompt(gem_name, variables)

    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Total time for {iterations} iterations: {duration:.4f} seconds")
    print(f"Average time per iteration: {(duration / iterations) * 1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
