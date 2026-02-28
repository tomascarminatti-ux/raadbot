
import time
import os
import sys

# Añadir el directorio raíz al path para poder importar agent
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt

def benchmark():
    gem_name = "gem1"
    variables = {
        "search_id": "SEARCH-123",
        "candidate_id": "CAND-456",
        "cv_text": "Este es un CV de prueba con bastante texto para simular un caso real " * 100,
        "interview_notes": "Notas de entrevista detalladas " * 50,
        "gem5_summary": {"objetivo": "Encontrar un líder", "desafios": ["Escalabilidad", "Cultura"]}
    }

    # Warmup
    for _ in range(10):
        build_prompt(gem_name, variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt(gem_name, variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Average time per build_prompt: {avg_time:.6f} seconds ({avg_time*1000:.4f} ms)")

if __name__ == "__main__":
    benchmark()
