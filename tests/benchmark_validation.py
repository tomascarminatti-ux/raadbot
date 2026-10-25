import json
import time
from jsonschema import validate
from agent.pipeline import Pipeline


def main():
    p = Pipeline(None, "SEARCH-2026-001", "/tmp/test_out")
    schema = p.schema

    with open("templates/output_example.json", "r", encoding="utf-8") as f:
        sample_data = json.load(f)

    iterations = 1000

    # Benchmark default jsonschema.validate call
    start = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    uncompiled_time = time.perf_counter() - start

    # Benchmark compiled validator call
    start = time.perf_counter()
    for _ in range(iterations):
        p.validator.validate(sample_data)
    compiled_time = time.perf_counter() - start

    speedup = uncompiled_time / compiled_time if compiled_time > 0 else 0
    print(f"Uncompiled jsonschema.validate ({iterations} runs): {uncompiled_time:.4f}s")
    print(f"Compiled validator.validate ({iterations} runs):   {compiled_time:.4f}s")
    print(f"Speedup: {speedup:.2f}x faster")


if __name__ == "__main__":
    main()
