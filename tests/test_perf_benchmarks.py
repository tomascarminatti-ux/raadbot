import os
import json
import time
import pytest
from utils.gem_core import validate_contract, _load_contract
from agent.prompt_builder import load_prompt, clear_prompt_caches, build_prompt

def test_contract_caching_and_performance():
    # Setup temporary contract
    contract = {
        "name": "string",
        "score": "number",
        "is_active": "boolean",
        "tags": "array",
        "metadata": "object"
    }
    contract_path = "tests/temp_perf_contract.json"
    os.makedirs("tests", exist_ok=True)
    with open(contract_path, "w") as f:
        json.dump(contract, f)

    valid_data = {
        "name": "Test",
        "score": 0.9,
        "is_active": True,
        "tags": ["a", "b"],
        "metadata": {"key": "value"}
    }

    # 1. Verification of correctness
    assert validate_contract(valid_data, contract_path) is True

    # Check that cache is working
    _load_contract.cache_clear()
    info_before = _load_contract.cache_info()
    assert info_before.hits == 0

    # First call: cache miss
    validate_contract(valid_data, contract_path)
    info_after_1 = _load_contract.cache_info()
    assert info_after_1.misses == 1

    # Second call: cache hit
    validate_contract(valid_data, contract_path)
    info_after_2 = _load_contract.cache_info()
    assert info_after_2.hits == 1

    # 2. Benchmark contract validation
    # Measure time for 200 uncached calls (using cache_clear in between)
    start_uncached = time.perf_counter()
    for _ in range(200):
        _load_contract.cache_clear()
        validate_contract(valid_data, contract_path)
    end_uncached = time.perf_counter()
    uncached_duration = (end_uncached - start_uncached) * 1000 / 200

    # Measure time for 2000 cached calls
    start_cached = time.perf_counter()
    for _ in range(2000):
        validate_contract(valid_data, contract_path)
    end_cached = time.perf_counter()
    cached_duration = (end_cached - start_cached) * 1000 / 2000

    print(f"\n[Contract Validation Benchmark]")
    print(f"Uncached avg: {uncached_duration:.4f} ms")
    print(f"Cached avg: {cached_duration:.4f} ms")
    print(f"Speedup: {uncached_duration / cached_duration:.2f}x")

    # Cleanup
    if os.path.exists(contract_path):
        os.remove(contract_path)

def test_prompt_caching_and_performance():
    # 1. Verification of correctness & cache clearing
    load_prompt.cache_clear()
    info_before = load_prompt.cache_info()
    assert info_before.hits == 0

    # First call to load "gem5" prompt: miss
    prompt1 = load_prompt("gem5")
    assert load_prompt.cache_info().misses == 1

    # Second call to load "gem5" prompt: hit
    prompt2 = load_prompt("gem5")
    assert load_prompt.cache_info().hits == 1
    assert prompt1 == prompt2

    # Clear cache
    clear_prompt_caches()
    assert load_prompt.cache_info().hits == 0
    assert load_prompt.cache_info().misses == 0

    # 2. Benchmark prompt building / loading
    # Measure uncached load_prompt (using cache_clear)
    start_uncached = time.perf_counter()
    for _ in range(200):
        load_prompt.cache_clear()
        load_prompt("gem5")
    end_uncached = time.perf_counter()
    uncached_duration = (end_uncached - start_uncached) * 1000 / 200

    # Measure cached load_prompt
    start_cached = time.perf_counter()
    for _ in range(2000):
        load_prompt("gem5")
    end_cached = time.perf_counter()
    cached_duration = (end_cached - start_cached) * 1000 / 2000

    print(f"\n[Prompt Loading Benchmark]")
    print(f"Uncached avg: {uncached_duration:.4f} ms")
    print(f"Cached avg: {cached_duration:.4f} ms")
    print(f"Speedup: {uncached_duration / cached_duration:.2f}x")
