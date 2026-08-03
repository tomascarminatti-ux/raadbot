import time
from utils.gem_core import validate_contract, _load_contract_cached
from agent.prompt_builder import load_prompt, _load_prompt_cached


def benchmark_prompt_loading(iterations=1000):
    gem_name = "gem1"

    # 1. Measure uncached (by clearing the cache before every call)
    start_time = time.perf_counter()
    for _ in range(iterations):
        _load_prompt_cached.cache_clear()
        load_prompt(gem_name)
    uncached_duration = time.perf_counter() - start_time

    # 2. Measure cached
    _load_prompt_cached.cache_clear()
    start_time = time.perf_counter()
    for _ in range(iterations):
        load_prompt(gem_name)
    cached_duration = time.perf_counter() - start_time

    speedup = uncached_duration / cached_duration if cached_duration > 0 else 0
    print(f"--- Prompt Loading Benchmark ({iterations} iterations) ---")
    print(f"Uncached Time: {uncached_duration:.4f} seconds")
    print(f"Cached Time:   {cached_duration:.4f} seconds")
    print(f"Speedup:       {speedup:.2f}x faster")
    return uncached_duration, cached_duration, speedup


def benchmark_contract_validation(iterations=2000):
    contract_path = "contracts/gem1_output.schema.json"
    dummy_data = {
        "discovery_dataset": ["item1", "item2"],
        "confidence_score": 0.95,
        "execution_metadata": {"elapsed_time": 120},
    }

    # 1. Measure uncached (by clearing the cache before every call)
    start_time = time.perf_counter()
    for _ in range(iterations):
        _load_contract_cached.cache_clear()
        validate_contract(dummy_data, contract_path)
    uncached_duration = time.perf_counter() - start_time

    # 2. Measure cached
    _load_contract_cached.cache_clear()
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(dummy_data, contract_path)
    cached_duration = time.perf_counter() - start_time

    speedup = uncached_duration / cached_duration if cached_duration > 0 else 0
    print(f"--- Contract Validation Benchmark ({iterations} iterations) ---")
    print(f"Uncached Time: {uncached_duration:.4f} seconds")
    print(f"Cached Time:   {cached_duration:.4f} seconds")
    print(f"Speedup:       {speedup:.2f}x faster")
    return uncached_duration, cached_duration, speedup


if __name__ == "__main__":
    print("Starting Performance Optimization Benchmarks...")
    benchmark_prompt_loading()
    print()
    benchmark_contract_validation()
