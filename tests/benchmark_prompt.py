import os
import time
import re
from agent.prompt_builder import PROMPTS_DIR, build_prompt


def load_prompt_uncached(gem_name: str) -> str:
    filepath = os.path.join(PROMPTS_DIR, f"{gem_name}.md")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt_uncached(gem_name: str, variables: dict) -> str:
    maestro = load_prompt_uncached("00_prompt_maestro")
    prompt = load_prompt_uncached(gem_name)
    prompt = prompt.replace("{{PROMPT_MAESTRO}}", maestro)
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        prompt = prompt.replace(placeholder, str(value))
    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
    if remaining:
        remaining = [v for v in remaining if v != "VERSION"]
    return prompt


def run_benchmark():
    vars_sample = {"candidate_name": "John Doe", "job_title": "Senior Engineer"}
    iterations = 5000

    # Uncached
    t0 = time.perf_counter()
    for _ in range(iterations):
        build_prompt_uncached("gem1", vars_sample)
    t1 = time.perf_counter()

    # Cached (via agent.prompt_builder)
    t2 = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", vars_sample)
    t3 = time.perf_counter()

    uncached_time = t1 - t0
    cached_time = t3 - t2
    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print(f"Benchmark results ({iterations} iterations):")
    print(f"  Uncached prompt building: {uncached_time:.4f}s")
    print(f"  Cached prompt building:   {cached_time:.4f}s")
    print(f"  Speedup achieved:         {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
