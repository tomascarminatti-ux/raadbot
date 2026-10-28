import time
from agent.prompt_builder import load_prompt, build_prompt, _load_prompt_cached


def main():
    print("⚡ Running Prompt Loading Benchmark...")

    # Benchmark cached loading (hits)
    _load_prompt_cached.cache_clear()

    # Warmup
    load_prompt("gem1")
    load_prompt("00_prompt_maestro")

    iterations = 2000
    start = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem1")
        load_prompt("00_prompt_maestro")
    cached_time = time.perf_counter() - start

    # Benchmark uncached loading by clearing cache on each iteration
    _load_prompt_cached.cache_clear()
    start = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        load_prompt("gem1")
        load_prompt("00_prompt_maestro")
    uncached_time = time.perf_counter() - start

    speedup = uncached_time / cached_time if cached_time > 0 else 0

    print(f"Uncached {iterations * 2} loads: {uncached_time * 1000:.2f} ms")
    print(f"Cached {iterations * 2} loads:   {cached_time * 1000:.2f} ms")
    print(f"⚡ Performance Speedup: {speedup:.2f}x faster")


if __name__ == "__main__":
    main()
