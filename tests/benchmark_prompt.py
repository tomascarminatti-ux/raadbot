import time
from agent.prompt_builder import load_prompt, build_prompt, _load_prompt_cached


def benchmark_prompt_loading():
    print("Running Prompt Builder Benchmark...")

    # Clear cache to measure cold load vs cached load
    _load_prompt_cached.cache_clear()

    t0 = time.perf_counter()
    for _ in range(1000):
        _load_prompt_cached.cache_clear()
        p = load_prompt("gem1")
    t1 = time.perf_counter()
    uncached_time = (t1 - t0) * 1000

    t0 = time.perf_counter()
    for _ in range(1000):
        p = load_prompt("gem1")
    t1 = time.perf_counter()
    cached_time = (t1 - t0) * 1000

    print(f"1,000 uncached load_prompt calls: {uncached_time:.2f} ms")
    print(f"1,000 cached load_prompt calls: {cached_time:.2f} ms")
    if cached_time > 0:
        print(f"Speedup: {uncached_time / cached_time:.2f}x")

    vars = {
        "search_id": "SEARCH-2024-001",
        "candidate_id": "CAND-001",
        "cv_text": "Experienced executive leader in tech.",
        "interview_notes": "Strong background in operational management.",
        "gem5_summary": "High potential search target.",
    }

    t0 = time.perf_counter()
    for _ in range(5000):
        b = build_prompt("gem1", vars)
    t1 = time.perf_counter()
    build_time = (t1 - t0) * 1000

    print(f"5,000 build_prompt calls: {build_time:.2f} ms")


if __name__ == "__main__":
    benchmark_prompt_loading()
