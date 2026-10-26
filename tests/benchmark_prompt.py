"""
benchmark_prompt.py – Benchmark para medir la mejora de rendimiento del caché en agent/prompt_builder.py.
"""

import os
import time
from agent.prompt_builder import load_prompt, _load_prompt_cached, PROMPTS_DIR


def uncached_load_prompt(gem_name: str) -> str:
    """Carga prompt directamente desde disco sin usar caché."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def main():
    iterations = 5000
    gem_name = "gem1"

    # Pre-warm cached load so first run isn't skewed
    load_prompt(gem_name)

    # 1. Medir sin caché
    t0 = time.perf_counter()
    for _ in range(iterations):
        uncached_load_prompt(gem_name)
    t1 = time.perf_counter()
    uncached_time = t1 - t0

    # 2. Medir con caché
    t2 = time.perf_counter()
    for _ in range(iterations):
        load_prompt(gem_name)
    t3 = time.perf_counter()
    cached_time = t3 - t2

    speedup = uncached_time / cached_time if cached_time > 0 else 0.0

    print(f"📊 Benchmark Results ({iterations} iterations):")
    print(f"  • Uncached time: {uncached_time:.4f}s")
    print(f"  • Cached time:   {cached_time:.4f}s")
    print(f"  • Speedup:       {speedup:.2f}x faster")

    assert speedup > 1.5, f"Expected speedup > 1.5x, got {speedup:.2f}x"
    print("✅ Benchmark passed!")


if __name__ == "__main__":
    main()
