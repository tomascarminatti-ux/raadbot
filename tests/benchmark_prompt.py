import os
import time
import functools
import re
from agent.prompt_builder import PROMPTS_DIR, build_prompt, _load_prompt_cached


def load_prompt_uncached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
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
    return prompt


def main():
    print("=== Prompt Loading Performance Benchmark ===")

    # Warmup
    _load_prompt_cached.cache_clear()
    build_prompt("gem1", {"jd_text": "Engineer", "candidate": "John"})

    N = 10000

    # Test uncached
    start = time.perf_counter()
    for _ in range(N):
        build_prompt_uncached("gem1", {"jd_text": "Engineer", "candidate": "John"})
    end = time.perf_counter()
    t_uncached = end - start

    # Test cached
    start = time.perf_counter()
    for _ in range(N):
        build_prompt("gem1", {"jd_text": "Engineer", "candidate": "John"})
    end = time.perf_counter()
    t_cached = end - start

    speedup = t_uncached / t_cached if t_cached > 0 else 0
    print(f"Iterations: {N}")
    print(f"Uncached Time: {t_uncached:.4f} seconds")
    print(f"Cached Time:   {t_cached:.4f} seconds")
    print(f"Speedup:       {speedup:.2f}x")

    assert speedup > 2.0, f"Expected speedup > 2x, got {speedup:.2f}x"


if __name__ == "__main__":
    main()
