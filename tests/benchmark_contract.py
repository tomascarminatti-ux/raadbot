import json
import timeit
from utils.gem_core import validate_contract, _load_contract_cached


def run_benchmark():
    contract_path = "contracts/gem1_output.schema.json"
    sample_data = {
        "discovery_dataset": ["test"],
        "confidence_score": 0.95,
        "execution_metadata": {"time": 10}
    }

    # Baseline: without cache
    def validate_uncached(data, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                contract = json.load(f)
            for k, expected_type in contract.items():
                if k not in data:
                    return False
            return True
        except Exception:
            return False

    iterations = 20000

    # Warmup
    validate_uncached(sample_data, contract_path)
    validate_contract(sample_data, contract_path)

    t_uncached = timeit.timeit(
        lambda: validate_uncached(sample_data, contract_path),
        number=iterations,
    )
    t_cached = timeit.timeit(
        lambda: validate_contract(sample_data, contract_path),
        number=iterations,
    )

    speedup = t_uncached / t_cached
    print(f"Contract Validation Benchmark ({iterations} iterations):")
    print(f"  Uncached: {t_uncached:.4f}s")
    print(f"  Cached:   {t_cached:.4f}s")
    print(f"  Speedup:  {speedup:.2f}x")
    print(f"  Cache info: {_load_contract_cached.cache_info()}")


if __name__ == "__main__":
    run_benchmark()
