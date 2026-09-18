import time
import os
import functools

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

def load_prompt_uncached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

@functools.lru_cache(maxsize=32)
def _load_prompt_cached(filepath: str, mtime: float) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_prompt_cached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    mtime = os.path.getmtime(filepath)
    return _load_prompt_cached(filepath, mtime)

def run_benchmark(iterations: int = 2000):
    print(f"Running benchmark with {iterations} iterations...")

    # Warmup
    load_prompt_uncached("gem1")
    load_prompt_cached("gem1")

    # Uncached
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt_uncached("gem1")
    t_uncached = time.perf_counter() - start

    # Cached
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt_cached("gem1")
    t_cached = time.perf_counter() - start

    speedup = t_uncached / t_cached if t_cached > 0 else 0.0

    print(f"Uncached prompt loading time: {t_uncached:.5f}s")
    print(f"Cached prompt loading time:   {t_cached:.5f}s")
    print(f"Speedup:                       {speedup:.2f}x")

    return speedup

if __name__ == "__main__":
    run_benchmark()
