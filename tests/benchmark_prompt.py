"""
benchmark_prompt.py - Script de benchmark para medir el rendimiento de build_prompt con y sin caché.
"""

import time
import os
import functools
import re
import json

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")


def load_prompt_uncached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
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
        if isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False, indent=2)
        prompt = prompt.replace(placeholder, str(value))
    remaining = re.findall(r"\{\{(\w+)\}\}", prompt)
    if remaining:
        remaining = [v for v in remaining if v != "VERSION"]
    return prompt


def run_benchmark(iterations: int = 2000):
    from agent.prompt_builder import build_prompt as build_prompt_cached

    vars_test = {
        "search_id": "SEARCH-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced engineer CV text...",
        "interview_notes": "Strong background in Python and FastAPI.",
        "gem5_summary": {"role": "Senior Engineer", "challenge": "High scale"},
    }

    # Warmup
    build_prompt_uncached("gem1", vars_test)
    build_prompt_cached("gem1", vars_test)

    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt_uncached("gem1", vars_test)
    t_uncached = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt_cached("gem1", vars_test)
    t_cached = time.perf_counter() - start

    speedup = t_uncached / t_cached if t_cached > 0 else 0
    print(f"--- BENCHMARK RESULTS ({iterations} iterations) ---")
    print(f"Uncached execution time: {t_uncached:.4f}s")
    print(f"Cached execution time:   {t_cached:.4f}s")
    print(f"Speedup:                {speedup:.2f}x faster")


if __name__ == "__main__":
    run_benchmark()
