import time
from utils.gem_core import validate_contract, _load_contract_cached

def benchmark():
    data = {"discovery_dataset": ["item1"], "confidence_score": 0.9, "execution_metadata": {}}
    contract_path = "contracts/gem1_output.schema.json"
    iterations = 1000

    # Test with cache
    _load_contract_cached.cache_clear()
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    t_cached = time.perf_counter() - t0

    print(f"Time taken for {iterations} validations with LRU cache: {t_cached:.5f}s")
    print(f"Cache info: {_load_contract_cached.cache_info()}")

if __name__ == "__main__":
    benchmark()
