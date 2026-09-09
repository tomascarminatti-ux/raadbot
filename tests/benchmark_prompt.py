import os
import time
import re
from agent.prompt_builder import load_prompt, clear_prompt_caches, PROMPTS_DIR


def benchmark():
    gem_name = "gem1"
    filepath = os.path.join(PROMPTS_DIR, f"{gem_name}.md")
    iterations = 5000

    if not os.path.exists(filepath):
        print(f"Prompt file {filepath} not found for benchmarking.")
        return

    # Uncached disk reads benchmark
    clear_prompt_caches()
    t0 = time.perf_counter()
    for _ in range(iterations):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        re.findall(r"\{\{(\w+)\}\}", content)
    t_uncached = time.perf_counter() - t0

    # Cached load_prompt benchmark
    clear_prompt_caches()
    # Warmup
    load_prompt(gem_name)

    t0 = time.perf_counter()
    for _ in range(iterations):
        load_prompt(gem_name)
    t_cached = time.perf_counter() - t0

    speedup = t_uncached / t_cached if t_cached > 0 else 0
    print(f"--- Prompt Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached Time : {t_uncached:.4f} seconds")
    print(f"Cached Time   : {t_cached:.4f} seconds")
    print(f"Speedup Factor: {speedup:.2f}x faster")


if __name__ == "__main__":
    benchmark()
