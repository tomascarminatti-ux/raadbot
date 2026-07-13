import time
import os
import sys
import json
import re

# Ensure we can import from the root directory
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt, load_prompt, load_maestro

def test_functionality():
    # Use a dummy prompt to test instead of gem6.md which might not have the expected placeholders
    dummy_prompt_path = "prompts/test_dummy.md"
    os.makedirs("prompts", exist_ok=True)
    with open(dummy_prompt_path, "w") as f:
        f.write("Maestro: {{PROMPT_MAESTRO}}\nVar: {{test_var}}\nMissing: {{missing_var}}\nVersion: {{VERSION}}")

    try:
        variables = {
            "test_var": "Hello World",
            "other": "Not used"
        }

        output = build_prompt("test_dummy", variables)

        maestro = load_maestro()
        assert maestro in output
        assert "Var: Hello World" in output
        assert "Missing: {{missing_var}}" in output
        assert "Version: {{VERSION}}" in output

        print("Functionality check passed!")
    finally:
        if os.path.exists(dummy_prompt_path):
            os.remove(dummy_prompt_path)

    return output

def run_benchmark():
    # Use gem6 for benchmark as it's a real world example
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-candidate",
        "context": {
            "search_inputs": {"jd": "Software Engineer"},
            "candidate_data": {"cv": "Experienced Python Developer"},
            "working_memory": [{"step": 1, "thought": "Thinking...", "observation": "Observed"}]
        }
    }

    # Warmup
    for _ in range(10):
        build_prompt("gem6", variables)

    start = time.perf_counter()
    iterations = 500
    for _ in range(iterations):
        build_prompt("gem6", variables)
    end = time.perf_counter()

    avg_time = (end - start) / iterations
    print(f"Average time over {iterations} iterations: {avg_time:.6f}s")
    return avg_time

if __name__ == "__main__":
    print("Starting verification...")
    original_output = test_functionality()
    print("Running benchmark...")
    run_benchmark()

    # Save original output for comparison later
    os.makedirs("tests", exist_ok=True)
    with open("tests/original_prompt_output_dummy.txt", "w") as f:
        f.write(original_output)
