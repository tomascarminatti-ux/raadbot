import time
import os
import sys

# Ensure root directory in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.prompt_builder import build_prompt, _load_prompt_cached

def benchmark():
    iterations = 2000
    test_vars = {"candidate_id": "CAND-999", "jd_text": "Sample JD", "cv_text": "Sample CV"}

    # Measure performance with caching enabled
    _load_prompt_cached.cache_clear()
    start_cached = time.perf_counter()
    for _ in range(iterations):
        build_prompt("gem1", test_vars)
    elapsed_cached = time.perf_counter() - start_cached

    # Measure performance bypassing cache (cache_clear on every iteration)
    start_uncached = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        build_prompt("gem1", test_vars)
    elapsed_uncached = time.perf_counter() - start_uncached

    speedup = elapsed_uncached / elapsed_cached if elapsed_cached > 0 else 0.0

    print(f"=== PROMPT LOADING BENCHMARK ({iterations} iterations) ===")
    print(f"Uncached execution time: {elapsed_uncached:.4f} seconds ({elapsed_uncached/iterations*1000:.4f} ms/op)")
    print(f"Cached execution time:   {elapsed_cached:.4f} seconds ({elapsed_cached/iterations*1000:.4f} ms/op)")
    print(f"Speedup factor:          {speedup:.2f}x faster")
    print("=========================================================")

if __name__ == "__main__":
    benchmark()
