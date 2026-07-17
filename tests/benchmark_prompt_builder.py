"""
benchmark_prompt_builder.py – Mide y compara el rendimiento de la construcción de prompts y la carga de esquemas.
"""

import time
import os
from agent.prompt_builder import build_prompt, clear_prompt_caches, load_prompt, load_maestro
from agent.pipeline import _get_cached_schema


def run_benchmark():
    print("=" * 60)
    print("🚀 INICIANDO BENCHMARK DE OPTIMIZACIONES DE PERFOMANCE")
    print("=" * 60)

    # Variables de prueba
    variables = {
        "search_id": "BENCH-2026-001",
        "candidate_id": "CAND-XYZ",
        "cv_text": "Este es un CV largo para probar la velocidad de reemplazo.",
        "interview_notes": "Notas de entrevista detalladas.",
        "gem5_summary": "Resumen de rol con desafíos clave.",
    }

    # --- 1. PROMPT BUILDER BENCHMARK ---
    print("\n[1] Probando `build_prompt` (GEM1)...")

    # Medir rendimiento SIN cache (limpiando cache en cada ciclo)
    iterations = 100
    start_time = time.perf_counter()
    for _ in range(iterations):
        clear_prompt_caches()
        _ = build_prompt("gem1", variables)
    duration_uncached = time.perf_counter() - start_time
    avg_uncached = (duration_uncached / iterations) * 1000

    # Medir rendimiento CON cache (deja que lru_cache y single-pass regex hagan su magia)
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = build_prompt("gem1", variables)
    duration_cached = time.perf_counter() - start_time
    avg_cached = (duration_cached / iterations) * 1000

    speedup_prompt = duration_uncached / duration_cached

    print(f"  - Sin Caché (I/O de disco + Reemplazos secuenciales): {avg_uncached:.4f} ms por llamada")
    print(f"  - Con Caché (LRU + Single-Pass Regex): {avg_cached:.4f} ms por llamada")
    print(f"  ⚡ SPEEDUP PROMPT BUILDER: {speedup_prompt:.2f}x más rápido!")

    # --- 2. SCHEMA LOADING BENCHMARK ---
    print("\n[2] Probando carga de esquema JSON...")

    schema_path = os.path.join(
        os.path.dirname(__file__), "..", "schemas", "gem_output.schema.json"
    )

    # Medir rendimiento SIN cache
    start_time = time.perf_counter()
    for _ in range(iterations):
        _get_cached_schema.cache_clear()
        _ = _get_cached_schema(schema_path)
    duration_schema_uncached = time.perf_counter() - start_time
    avg_schema_uncached = (duration_schema_uncached / iterations) * 1000

    # Medir rendimiento CON cache
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = _get_cached_schema(schema_path)
    duration_schema_cached = time.perf_counter() - start_time
    avg_schema_cached = (duration_schema_cached / iterations) * 1000

    speedup_schema = duration_schema_uncached / duration_schema_cached

    print(f"  - Sin Caché (Lectura I/O de disco del JSON): {avg_schema_uncached:.4f} ms por llamada")
    print(f"  - Con Caché (lru_cache): {avg_schema_cached:.4f} ms por llamada")
    print(f"  ⚡ SPEEDUP SCHEMA LOADING: {speedup_schema:.2f}x más rápido!")

    print("\n" + "=" * 60)
    print("🎯 BENCHMARK COMPLETADO EXITOSAMENTE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_benchmark()
