import os
import time
import json
from agent.prompt_builder import load_prompt, PROMPTS_DIR
from utils.gem_core import validate_contract


def load_prompt_raw(gem_name: str) -> str:
    """Old uncached prompt loader."""
    filename = f"{gem_name}.md"
    filepath = os.path.join(PROMPTS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def validate_contract_raw(data: dict, contract_path: str) -> bool:
    """Old uncached contract validator."""
    try:
        with open(contract_path, "r") as f:
            contract = json.load(f)
        for key in contract:
            if not isinstance(key, str):
                continue
            expected_type = contract[key]
            if key not in data:
                return False
            val = data.get(key)
            if expected_type == "array" and not isinstance(val, list): return False
            if expected_type == "number" and not isinstance(val, (int, float)): return False
            if expected_type == "string" and not isinstance(val, str): return False
            if expected_type == "object" and not isinstance(val, dict): return False
            if expected_type == "boolean" and not isinstance(val, bool): return False
        return True
    except Exception:
        return False


def run_benchmarks():
    print("=================== PERFORMANCE BENCHMARKS ===================")

    # 1. Prompt Loading Benchmark
    print("\n[1] Benchmarking Prompt Loading (1,000 iterations)...")

    # Warmup
    load_prompt_raw("gem1")
    load_prompt("gem1")

    start_raw = time.perf_counter()
    for _ in range(1000):
        load_prompt_raw("gem1")
    end_raw = time.perf_counter()
    raw_time = end_raw - start_raw

    start_cached = time.perf_counter()
    for _ in range(1000):
        load_prompt("gem1")
    end_cached = time.perf_counter()
    cached_time = end_cached - start_cached

    speedup_prompt = raw_time / cached_time
    print(f"Uncached load_prompt: {raw_time:.5f}s (avg: {raw_time*1000:.3f} microseconds)")
    print(f"Cached load_prompt:   {cached_time:.5f}s (avg: {cached_time*1000:.3f} microseconds)")
    print(f"Prompt Loading Speedup: {speedup_prompt:.2f}x faster!")

    # 2. Contract Validation Benchmark
    print("\n[2] Benchmarking Contract Validation (1,000 iterations)...")

    # Create temp contract
    contract_data = {
        "name": "string",
        "score": "number",
        "is_active": "boolean"
    }
    contract_path = "tests/temp_bench_contract.json"
    with open(contract_path, "w") as f:
        json.dump(contract_data, f)

    test_payload = {"name": "Test User", "score": 95.5, "is_active": True}

    # Warmup
    validate_contract_raw(test_payload, contract_path)
    validate_contract(test_payload, contract_path)

    start_raw_cv = time.perf_counter()
    for _ in range(1000):
        validate_contract_raw(test_payload, contract_path)
    end_raw_cv = time.perf_counter()
    raw_cv_time = end_raw_cv - start_raw_cv

    start_cached_cv = time.perf_counter()
    for _ in range(1000):
        validate_contract(test_payload, contract_path)
    end_cached_cv = time.perf_counter()
    cached_cv_time = end_cached_cv - start_cached_cv

    speedup_cv = raw_cv_time / cached_cv_time
    print(f"Uncached validate_contract: {raw_cv_time:.5f}s (avg: {raw_cv_time*1000:.3f} microseconds)")
    print(f"Cached validate_contract:   {cached_cv_time:.5f}s (avg: {cached_cv_time*1000:.3f} microseconds)")
    print(f"Contract Validation Speedup: {speedup_cv:.2f}x faster!")

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)

    print("\n==============================================================")


if __name__ == "__main__":
    run_benchmarks()
