import time
import os
import functools
import re
from agent.prompt_builder import build_prompt, PROMPTS_DIR


def build_prompt_uncached(gem_name: str, variables: dict) -> str:
    """Implementación de referencia sin caché ni regex precompilado."""
    maestro_path = os.path.join(PROMPTS_DIR, "00_prompt_maestro.md")
    gem_path = os.path.join(PROMPTS_DIR, f"{gem_name}.md")

    with open(maestro_path, "r", encoding="utf-8") as f:
        maestro = f.read()
    with open(gem_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        prompt = prompt.replace(placeholder, str(value))

    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
    if remaining:
        remaining = [v for v in remaining if v != "VERSION"]

    return prompt


def run_benchmark(iterations: int = 3000):
    sample_inputs = {"input": "Candidate CV text for Senior Engineer position."}

    # Warmup cached implementation
    build_prompt("gem5", sample_inputs)

    # Benchmark Uncached
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt_uncached("gem5", sample_inputs)
    uncached_time = time.perf_counter() - start

    # Benchmark Cached
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem5", sample_inputs)
    cached_time = time.perf_counter() - start

    speedup = uncached_time / cached_time if cached_time > 0 else 0
    print(f"\n--- Prompt Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached execution time: {uncached_time:.4f}s")
    print(f"Cached execution time:   {cached_time:.4f}s")
    print(f"Speedup factor:          {speedup:.2f}x faster\n")


if __name__ == "__main__":
    run_benchmark()
