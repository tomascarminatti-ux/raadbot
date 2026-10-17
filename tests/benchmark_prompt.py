import time
import os
from agent.prompt_builder import build_prompt, _load_prompt_cached, PROMPTS_DIR


def benchmark():
    iterations = 5000

    # Measure uncached disk reads by reading directly from file
    start = time.perf_counter()
    for _ in range(iterations):
        for name in ["00_prompt_maestro.md", "gem1.md"]:
            filepath = os.path.join(PROMPTS_DIR, name)
            with open(filepath, "r", encoding="utf-8") as f:
                f.read()
    uncached_time = time.perf_counter() - start

    # Measure cached reads
    _load_prompt_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", {"jd_text": "Software Engineer", "company_context": "Tech Corp"})
    cached_time = time.perf_counter() - start

    speedup = uncached_time / cached_time if cached_time > 0 else 0
    print(f"Benchmark Results ({iterations} iterations):")
    print(f"  Uncached (Disk Reads): {uncached_time:.4f} seconds")
    print(f"  Cached (LRU Cache):   {cached_time:.4f} seconds")
    print(f"  Speedup:              {speedup:.2f}x")


if __name__ == "__main__":
    benchmark()
