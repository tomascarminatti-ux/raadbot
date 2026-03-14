import time
import os
import sys

# Add current dir to path to find agent/
sys.path.append(os.getcwd())

# flake8: noqa: E402
from agent.prompt_builder import build_prompt, load_prompt, load_maestro


def run_benchmark():
    """Quantifies the impact of lru_cache on prompt building."""
    print("🚀 Starting Bolt Performance Benchmark...")

    variables = {"input": {"role": "Engineer", "skills": ["Python", "AWS"]}}
    iterations = 1000

    # 1. Measure WITHOUT cache (by clearing it each time)
    start_time = time.time()
    for _ in range(iterations):
        load_prompt.cache_clear()
        load_maestro.cache_clear()
        build_prompt("gem5", variables)
    no_cache_time = time.time() - start_time
    avg_no_cache = (no_cache_time / iterations) * 1000

    # 2. Measure WITH cache
    # Warmup
    build_prompt("gem5", variables)

    start_time = time.time()
    for _ in range(iterations):
        build_prompt("gem5", variables)
    cache_time = time.time() - start_time
    avg_cache = (cache_time / iterations) * 1000

    print(f"\n📊 RESULTS (over {iterations} iterations):")
    print(f"  - Without cache: {avg_no_cache:.4f} ms/call")
    print(f"  - With cache:    {avg_cache:.4f} ms/call")
    print(f"  - Speedup:       {avg_no_cache / avg_cache:.2f}x")
    print(
        f"\n✅ Optimization verified: Reduced latency by "
        f"{avg_no_cache - avg_cache:.4f} ms per prompt build."
    )


if __name__ == "__main__":
    try:
        run_benchmark()
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        sys.exit(1)
