import time
import json
from jsonschema import validate, validators

def run_benchmark():
    schema_path = 'schemas/gem_output.schema.json'
    with open(schema_path) as f:
        schema = json.load(f)

    sample_data = {
        'meta': {
            'search_id': 'SEARCH-2025-001',
            'candidate_id': 'CAND-001',
            'gem': 'GEM_1',
            'prompt_version': 'v1.0',
            'timestamp': '2025-01-01T00:00:00Z',
            'sources': ['cv_text']
        },
        'scores': {'score_dimension': 8, 'confidence': 9},
        'blockers': [],
        'content': {'summary': 'test'}
    }

    iterations = 1000

    # Uncompiled jsonschema.validate
    t0 = time.perf_counter()
    for _ in range(iterations):
        validate(instance=sample_data, schema=schema)
    t1 = time.perf_counter()
    uncompiled_time = t1 - t0

    # Pre-compiled validator
    validator_cls = validators.validator_for(schema)
    validator = validator_cls(schema)

    t2 = time.perf_counter()
    for _ in range(iterations):
        validator.validate(sample_data)
    t3 = time.perf_counter()
    compiled_time = t3 - t2

    speedup = uncompiled_time / compiled_time if compiled_time > 0 else 0
    print(f"Benchmark ({iterations} iterations):")
    print(f"  - Uncompiled jsonschema.validate: {uncompiled_time:.4f}s")
    print(f"  - Pre-compiled validator:        {compiled_time:.4f}s")
    print(f"  - Speedup:                      {speedup:.2f}x")

if __name__ == "__main__":
    run_benchmark()
