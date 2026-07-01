import time
import os
import sys

# Añadir el path para que encuentre el paquete agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    variables = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Este es un CV de prueba con mucha información para simular carga real.",
        "interview_notes": "Notas de la entrevista que también ocupan espacio.",
        "gem5_summary": "Resumen de GEM5 que es un JSON stringificado habitualmente.",
        "data": {"key": "value", "nested": [1, 2, 3]}
    }

    # Warm up
    build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time to build prompt: {avg_time*1000:.4f} ms")

if __name__ == "__main__":
    benchmark()
