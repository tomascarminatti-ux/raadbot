import time
import os
import sys

# Add parent directory to path to import agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import load_prompt, build_prompt

def benchmark_load_prompt(iterations=1000):
    start_time = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem1")
    end_time = time.perf_counter()
    print(f"load_prompt('gem1') x {iterations}: {end_time - start_time:.4f}s")

def benchmark_build_prompt(iterations=100):
    variables = {"input": {"test": "data"}}
    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()
    print(f"build_prompt('gem1') x {iterations}: {end_time - start_time:.4f}s")

if __name__ == "__main__":
    # Ensure prompts exist
    os.makedirs("prompts", exist_ok=True)
    if not os.path.exists("prompts/gem1.md"):
        with open("prompts/gem1.md", "w") as f:
            f.write("# GEM1\n{{PROMPT_MAESTRO}}\n{{input}}")
    if not os.path.exists("prompts/00_prompt_maestro.md"):
        with open("prompts/00_prompt_maestro.md", "w") as f:
            f.write("# Maestro Prompt")

    print("Benchmarking BEFORE optimization...")
    benchmark_load_prompt()
    benchmark_build_prompt()
