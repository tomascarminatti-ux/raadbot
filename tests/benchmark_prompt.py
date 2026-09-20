import time
from agent.prompt_builder import load_prompt, _load_prompt_cached

def run_benchmark():
    # Cold cache run
    _load_prompt_cached.cache_clear()

    start_time = time.perf_counter()
    for _ in range(1000):
        _load_prompt_cached.cache_clear()
        load_prompt("gem1")
        load_prompt("gem2")
        load_prompt("gem3")
        load_prompt("gem4")
        load_prompt("gem5")
        load_prompt("00_prompt_maestro")
    uncached_duration = time.perf_counter() - start_time

    # Warm cache run
    _load_prompt_cached.cache_clear()
    load_prompt("gem1")
    load_prompt("gem2")
    load_prompt("gem3")
    load_prompt("gem4")
    load_prompt("gem5")
    load_prompt("00_prompt_maestro")

    start_time = time.perf_counter()
    for _ in range(1000):
        load_prompt("gem1")
        load_prompt("gem2")
        load_prompt("gem3")
        load_prompt("gem4")
        load_prompt("gem5")
        load_prompt("00_prompt_maestro")
    cached_duration = time.perf_counter() - start_time

    speedup = uncached_duration / cached_duration if cached_duration > 0 else float("inf")
    print(f"Uncached 6k loads: {uncached_duration:.4f}s")
    print(f"Cached 6k loads: {cached_duration:.4f}s")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    run_benchmark()
