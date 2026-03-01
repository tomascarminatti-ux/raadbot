import time
import sys
import os

# Añadir el directorio raíz al path para poder importar agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.prompt_builder import build_prompt

def benchmark_build_prompt(iterations=1000):
    variables = {
        "search_id": "TEST-123",
        "candidate_id": "CAND-001",
        "cv_text": "Este es un CV de prueba con mucha información para simular carga real. " * 100,
        "interview_notes": "Notas de entrevista simuladas. " * 50,
        "gem5_summary": {"key": "value", "description": "Resumen de GEM5 simulado"},
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        # Usamos gem1 como ejemplo
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    avg_time = (end_time - start_time) / iterations
    print(f"Benchmark build_prompt ({iterations} iteraciones):")
    print(f"  Tiempo total: {end_time - start_time:.4f}s")
    print(f"  Tiempo promedio: {avg_time*1000:.4f}ms")

if __name__ == "__main__":
    benchmark_build_prompt()
