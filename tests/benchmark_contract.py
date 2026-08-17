import time
import json
import tempfile
import os
from utils.gem_core import validate_contract, _load_contract_cached


def main():
    data = {
        "name": "Test Candidate",
        "score": 0.95,
        "is_active": True,
        "tags": ["senior", "engineer"],
        "metadata": {"source": "linkedin"},
    }
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object",
    }

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        json.dump(contract, f)
        contract_path = f.name

    try:
        # Warmup and initial call
        assert validate_contract(data, contract_path) is True

        # Measure 1,000 iterations
        iterations = 1000
        start = time.perf_counter()
        for _ in range(iterations):
            validate_contract(data, contract_path)
        elapsed = time.perf_counter() - start

        cache_info = _load_contract_cached.cache_info()
        print(f"Contract validation time for {iterations} iterations: {elapsed:.6f}s")
        print(f"LRU Cache Info: {cache_info}")
        assert cache_info.hits > 0, "Cache should record hits"

    finally:
        if os.path.exists(contract_path):
            os.remove(contract_path)


if __name__ == "__main__":
    main()
