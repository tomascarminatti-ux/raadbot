import time
import os
import sys

# Add the current directory to sys.path to import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=100):
    variables = {
        "search_id": "test-search",
        "candidate_id": "test-candidate",
        "context": {"key": "value" * 100}
    }

    start_time = time.time()
    for _ in range(iterations):
        # We use gem5 as it's likely to exist
        try:
            build_prompt("gem5", variables)
        except FileNotFoundError:
            # Fallback to creating a dummy prompt if gem5 doesn't exist
            os.makedirs("prompts", exist_ok=True)
            with open("prompts/dummy.md", "w") as f:
                f.write("Maestro: {{PROMPT_MAESTRO}}\nSearch: {{search_id}}\nContext: {{context}}")
            with open("prompts/00_prompt_maestro.md", "w") as f:
                f.write("I am the maestro.")
            build_prompt("dummy", variables)

    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average time per build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_build_prompt()
