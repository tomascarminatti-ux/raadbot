import time
from agent.prompt_builder import build_prompt, load_prompt, _load_prompt_cached


def benchmark_prompt_builder(iterations: int = 2000):
    vars = {
        "search_id": "BENCHMARK-001",
        "candidate_id": "CAND-001",
        "cv_text": "Sample CV content for benchmarking",
        "interview_notes": "Sample interview notes",
        "gem5_summary": "Sample GEM5 summary",
    }

    # 1. Uncached baseline (clear cache before every load_prompt call)
    start_time = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        build_prompt("gem1", vars)
    uncached_duration = time.perf_counter() - start_time

    # 2. Cached run
    _load_prompt_cached.cache_clear()
    # Warm up cache
    build_prompt("gem1", vars)

    start_time = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", vars)
    cached_duration = time.perf_counter() - start_time

    speedup = uncached_duration / cached_duration if cached_duration > 0 else 0.0

    print("=" * 60)
    print(f"Prompt Builder Benchmark ({iterations} iterations)")
    print(f"Uncached duration : {uncached_duration:.4f} seconds")
    print(f"Cached duration   : {cached_duration:.4f} seconds")
    print(f"Speedup factor    : {speedup:.2f}x faster")
    print("=" * 60)

    return speedup


if __name__ == "__main__":
    benchmark_prompt_builder()
