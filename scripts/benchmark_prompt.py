import time
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt  # noqa: E402


def benchmark_build_prompt(iterations=1000):
    gem_name = "gem1"
    variables = {
        "candidate": {
            "name": "Juan Perez",
            "experience": "10 years",
            "skills": ["Python", "FastAPI", "React"]
        },
        "mandate": "Senior Software Engineer",
        "search_context": "Madrid, Remote"
    }

    start_time = time.time()
    for _ in range(iterations):
        _ = build_prompt(gem_name, variables)
    end_time = time.time()

    total_time = end_time - start_time
    avg_time = total_time / iterations
    print(f"Total time for {iterations} iterations: {total_time:.4f}s")
    print(f"Average time per iteration: {avg_time*1000:.4f}ms")


if __name__ == "__main__":
    # Ensure prompts exist for the benchmark
    os.makedirs("prompts", exist_ok=True)
    if not os.path.exists("prompts/00_prompt_maestro.md"):
        with open("prompts/00_prompt_maestro.md", "w") as f:
            f.write("Maestro prompt content")
    if not os.path.exists("prompts/gem1.md"):
        with open("prompts/gem1.md", "w") as f:
            f.write("GEM1 content: {{PROMPT_MAESTRO}}, {{candidate}}, {{mandate}}, {{search_context}}")

    benchmark_build_prompt()
