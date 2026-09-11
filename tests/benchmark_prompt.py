import time
from agent.prompt_builder import build_prompt, clear_prompt_caches, _load_prompt_cached

def run_benchmark(iterations: int = 2000):
    vars = {
        "search_id": "BENCHMARK-SEARCH",
        "candidate_id": "BENCHMARK-CAND",
        "cv_text": "Experienced CTO with 10+ years in distributed systems.",
        "interview_notes": "Strong leadership skills, deep technical knowledge.",
        "gem5_summary": "High growth tech startup looking for scaling expertise.",
    }

    # 1. Benchmark uncached loading (by clearing cache on every iteration)
    start_time = time.perf_counter()
    for _ in range(iterations):
        clear_prompt_caches()
        _ = build_prompt("gem1", vars)
    uncached_duration = time.perf_counter() - start_time

    # 2. Benchmark cached loading
    clear_prompt_caches()
    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = build_prompt("gem1", vars)
    cached_duration = time.perf_counter() - start_time

    speedup = uncached_duration / cached_duration if cached_duration > 0 else 0

    print(f"\n--- Prompt Builder Performance Benchmark ({iterations:,} iterations) ---")
    print(f"Uncached execution time: {uncached_duration:.4f}s ({uncached_duration/iterations*1000:.4f} ms/iter)")
    print(f"Cached execution time:   {cached_duration:.4f}s ({cached_duration/iterations*1000:.4f} ms/iter)")
    print(f"Performance Speedup:     {speedup:.2f}x faster\n")

if __name__ == "__main__":
    run_benchmark()
