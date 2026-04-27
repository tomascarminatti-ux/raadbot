from agent.prompt_builder import build_prompt
import time
import sys
import os

# Add parent directory to path to import agent
sys.path.append(os.getcwd())


def benchmark():
    variables = {
        "search_id": "test-search",
        "candidate_id": "candidate-123",
        "context": {
            "name": "John Doe",
            "experience": "10 years",
            "skills": ["Python", "AI"]
        }
    }

    # Warm up
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.time()
    iterations = 100
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.time()

    avg_time = (end_time - start_time) / iterations
    print(f"Average build_prompt time: {avg_time*1000:.4f} ms")


if __name__ == "__main__":
    # Ensure prompts exist
    if not os.path.exists("prompts/gem1.md"):
        os.makedirs("prompts", exist_ok=True)
        with open("prompts/gem1.md", "w") as f:
            f.write(
                "Role: {{PROMPT_MAESTRO}}\nContext: {{context}}\nID: {{candidate_id}}")
    if not os.path.exists("prompts/00_prompt_maestro.md"):
        with open("prompts/00_prompt_maestro.md", "w") as f:
            f.write("I am the Maestro.")

    benchmark()
