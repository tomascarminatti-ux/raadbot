import time
import os
import sys

# Add the current directory to sys.path to import agent modules
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Este es un CV muy largo " * 100,
        "interview_notes": "Notas de entrevista " * 50,
        "gem5_summary": "Resumen de GEM5 " * 20,
    }

    # Warm up
    for _ in range(5):
        build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 100
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    # Create dummy prompts if they don't exist for testing
    os.makedirs("prompts", exist_ok=True)
    if not os.path.exists("prompts/00_prompt_maestro.md"):
        with open("prompts/00_prompt_maestro.md", "w") as f:
            f.write("Maestro Prompt Context")
    if not os.path.exists("prompts/gem1.md"):
        with open("prompts/gem1.md", "w") as f:
            f.write("GEM1 Prompt: {{PROMPT_MAESTRO}} {{cv_text}} {{interview_notes}} {{gem5_summary}}")

    benchmark()
