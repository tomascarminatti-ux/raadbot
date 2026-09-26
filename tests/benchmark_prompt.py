import os
import time
import functools

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

def load_prompt_uncached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

@functools.lru_cache(maxsize=32)
def _load_prompt_cached_internal(filepath: str, mtime: float) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def load_prompt_cached(gem_name: str) -> str:
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Prompt no encontrado: {filepath}")

    mtime = os.path.getmtime(filepath)
    return _load_prompt_cached_internal(filepath, mtime)

def benchmark():
    gem_names = ["gem1", "gem2", "gem3", "gem4", "gem5", "gem6", "00_prompt_maestro"]

    # Warmup
    for name in gem_names:
        load_prompt_uncached(name)
        load_prompt_cached(name)

    N = 20000

    t0 = time.perf_counter()
    for _ in range(N):
        for name in gem_names:
            load_prompt_uncached(name)
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    for _ in range(N):
        for name in gem_names:
            load_prompt_cached(name)
    t3 = time.perf_counter()

    uncached_time = t1 - t0
    cached_time = t3 - t2

    print(f"Uncached load_prompt time: {uncached_time:.4f}s")
    print(f"Cached load_prompt time:   {cached_time:.4f}s")
    print(f"Speedup:                   {uncached_time / cached_time:.2f}x")

if __name__ == "__main__":
    benchmark()
