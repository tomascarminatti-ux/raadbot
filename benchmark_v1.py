
import time
import os
import sys

# Add the current directory to sys.path to import agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark_build_prompt():
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Este es un CV muy largo " * 100,
        "interview_notes": "Notas de entrevista " * 50,
        "gem5_summary": "Resumen de GEM5 " * 20,
    }

    # Warmup
    for _ in range(10):
        build_prompt("gem1", variables)

    iterations = 1000
    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    try:
        benchmark_build_prompt()
    except Exception as e:
        print(f"Error: {e}")
