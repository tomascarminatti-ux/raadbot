import time
import os
import tempfile
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR


def test_load_prompt_lru_cache():
    """Verifica que load_prompt devuelva la versión en caché y que clear_prompt_caches invalide correctamente."""
    clear_prompt_caches()

    # Primera llamada debe cargar desde disco
    content1 = load_prompt("gem1")
    # Segunda llamada debe servir desde la memoria caché LRU
    content2 = load_prompt("gem1")

    assert content1 == content2
    assert load_prompt.cache_info().hits >= 1

    # Limpiar caché e instruir una nueva carga
    clear_prompt_caches()
    assert load_prompt.cache_info().hits == 0
    content3 = load_prompt("gem1")
    assert content3 == content1


def test_load_prompt_performance_benchmark():
    """Mide y verifica la mejora en tiempo de ejecución al usar caché LRU para la carga de plantillas."""
    clear_prompt_caches()

    iterations = 1000

    # Carga sin caché (limpiando caché en cada iteración)
    start_uncached = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem5")
        clear_prompt_caches()
    duration_uncached = time.perf_counter() - start_uncached

    # Carga con caché LRU
    clear_prompt_caches()
    start_cached = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem5")
    duration_cached = time.perf_counter() - start_cached

    # La carga en caché debe ser significativamente más rápida que la I/O de disco
    speedup = duration_uncached / (duration_cached if duration_cached > 0 else 1e-6)
    print(f"\n⚡ Prompt loading benchmark ({iterations} iterations):")
    print(f"   Uncached: {duration_uncached:.5f}s")
    print(f"   Cached:   {duration_cached:.5f}s")
    print(f"   Speedup:  {speedup:.2f}x")

    assert duration_cached < duration_uncached
