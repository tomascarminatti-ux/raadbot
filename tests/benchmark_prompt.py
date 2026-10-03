import time
from agent.prompt_builder import load_prompt, build_prompt, _load_prompt_cached

def run_benchmark():
    print("=== Prompt Loading Benchmark ===")

    # Measure uncached (by clearing cache each time)
    _load_prompt_cached.cache_clear()

    variables = {
        "jd_text": "Senior Developer",
        "kickoff_notes": "Strong Python knowledge required",
        "company_context": "Fast-growing AI startup"
    }

    N = 2000

    # Warmup
    build_prompt("gem1", variables)

    t0 = time.perf_counter()
    for _ in range(N):
        _load_prompt_cached.cache_clear()
        build_prompt("gem1", variables)
    t_uncached = time.perf_counter() - t0

    _load_prompt_cached.cache_clear()
    t0 = time.perf_counter()
    for _ in range(N):
        build_prompt("gem1", variables)
    t_cached = time.perf_counter() - t0

    speedup = t_uncached / t_cached if t_cached > 0 else 0.0
    print(f"Uncached {N} prompt builds: {t_uncached:.4f}s")
    print(f"Cached {N} prompt builds:   {t_cached:.4f}s")
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    run_benchmark()
