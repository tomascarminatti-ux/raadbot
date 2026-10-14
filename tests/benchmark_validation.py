import time
import os
import json
from unittest.mock import MagicMock
from jsonschema import validate
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark():
    mock_gemini = MagicMock(spec=GeminiClient)
    output_dir = "/tmp/benchmark_output"
    os.makedirs(output_dir, exist_ok=True)

    pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", output_dir)

    dummy_data = {
        "meta": {
            "search_id": "SEARCH-2026-001",
            "candidate_id": "CAND-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["cv_text"]
        },
        "scores": {
            "score_dimension": 8,
            "confidence": 9
        },
        "blockers": [],
        "content": {"test": "data"}
    }

    iterations = 5000

    # Uncompiled validation (jsonschema.validate)
    start_uncompiled = time.perf_counter()
    for _ in range(iterations):
        validate(instance=dummy_data, schema=pipeline.schema)
    end_uncompiled = time.perf_counter()
    uncompiled_total = end_uncompiled - start_uncompiled

    # Compiled validation (pipeline._validate_output using self.validator)
    start_compiled = time.perf_counter()
    for _ in range(iterations):
        pipeline._validate_output(dummy_data, "gem1")
    end_compiled = time.perf_counter()
    compiled_total = end_compiled - start_compiled

    speedup = uncompiled_total / compiled_total
    print(f"Iterations: {iterations}")
    print(f"Uncompiled jsonschema.validate total time: {uncompiled_total:.4f}s ({uncompiled_total/iterations*1000:.4f} ms/op)")
    print(f"Compiled self.validator.validate total time:   {compiled_total:.4f}s ({compiled_total/iterations*1000:.4f} ms/op)")
    print(f"Speedup: {speedup:.2f}x faster!")

if __name__ == "__main__":
    benchmark()
