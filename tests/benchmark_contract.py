import time
from utils.gem_core import validate_contract, _load_contract_cached


# We'll measure performance of validate_contract
def run_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    data = {
        "discovery_dataset": ["test"],
        "confidence_score": 0.8,
        "execution_metadata": {"key": "value"},
    }

    # Warmup
    validate_contract(data, contract_path)

    # 1. Benchmark without caching (simulated by clearing the cache if cached)
    start_time = time.perf_counter()
    iterations = 5000
    for _ in range(iterations):
        if hasattr(_load_contract_cached, "cache_clear"):
            _load_contract_cached.cache_clear()
        validate_contract(data, contract_path)
    end_time = time.perf_counter()
    time_without_cache = end_time - start_time
    print(
        f"Time without cache ({iterations} iterations): {time_without_cache:.4f} seconds"
    )

    # 2. Benchmark with caching
    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    end_time = time.perf_counter()
    time_with_cache = end_time - start_time
    print(f"Time with cache ({iterations} iterations): {time_with_cache:.4f} seconds")

    speedup = (
        time_without_cache / time_with_cache if time_with_cache > 0 else float("inf")
    )
    print(f"Speedup: {speedup:.2f}x")


if __name__ == "__main__":
    run_benchmark()
