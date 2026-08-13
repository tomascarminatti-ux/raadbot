import time
import os
import json
from agent.prompt_builder import load_prompt
from utils.gem_core import validate_contract

def test_benchmark_performance():
    # Setup files
    prompt_path = "prompts/gem1.md"
    contract_path = "contracts/gem1_output.schema.json"

    assert os.path.exists(prompt_path), "gem1.md prompt should exist"
    assert os.path.exists(contract_path), "gem1_output.schema.json should exist"

    iterations = 50

    # 1. Benchmark load_prompt
    start_time = time.perf_counter()
    for _ in range(iterations):
        load_prompt("gem1")
    duration_cached = time.perf_counter() - start_time
    print(f"\n[BENCHMARK] load_prompt: {iterations} iterations took {duration_cached:.6f} seconds.")

    # Let's compare with raw read (simulating non-cached version)
    start_time = time.perf_counter()
    for _ in range(iterations):
        with open(prompt_path, "r", encoding="utf-8") as f:
            f.read()
    duration_uncached = time.perf_counter() - start_time
    print(f"[BENCHMARK] raw read: {iterations} iterations took {duration_uncached:.6f} seconds.")

    speedup_prompt = duration_uncached / duration_cached if duration_cached > 0 else 0
    print(f"[BENCHMARK] Prompt loading speedup: {speedup_prompt:.2f}x")

    # 2. Benchmark validate_contract
    data = {
        "discovery_dataset": ["test"],
        "confidence_score": 0.95,
        "execution_metadata": {}
    }

    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract(data, contract_path)
    duration_validate_cached = time.perf_counter() - start_time
    print(f"[BENCHMARK] validate_contract (cached): {iterations} iterations took {duration_validate_cached:.6f} seconds.")

    # Simulating raw non-cached validation (loading from disk each time)
    def validate_contract_uncached(data, path):
        with open(path, "r") as f:
            contract = json.load(f)
        for key in contract:
            if key not in data:
                return False
        return True

    start_time = time.perf_counter()
    for _ in range(iterations):
        validate_contract_uncached(data, contract_path)
    duration_validate_uncached = time.perf_counter() - start_time
    print(f"[BENCHMARK] validate_contract (uncached): {iterations} iterations took {duration_validate_uncached:.6f} seconds.")

    speedup_contract = duration_validate_uncached / duration_validate_cached if duration_validate_cached > 0 else 0
    print(f"[BENCHMARK] Contract validation speedup: {speedup_contract:.2f}x")

    # Make assertion lenient so high-load environments don't flake, but print findings clearly
    assert speedup_prompt > 0.5
    assert speedup_contract > 0.5
