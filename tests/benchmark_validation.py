import time
import tempfile
from unittest.mock import MagicMock
import jsonschema

from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient


def benchmark_schema_validation():
    mock_gemini = MagicMock(spec=GeminiClient)
    with tempfile.TemporaryDirectory() as tmpdir:
        pipeline = Pipeline(mock_gemini, "SEARCH-2026-001", tmpdir)

        sample_data = {
            "meta": {
                "search_id": "SEARCH-2026-001",
                "gem": "GEM_1",
                "prompt_version": "v1.2",
                "timestamp": "2024-01-01T00:00:00Z",
                "sources": ["cv.txt"],
            },
            "scores": {"score_dimension": 8, "confidence": 9},
            "blockers": [],
            "content": {"test": "data"},
        }

        iterations = 2000

        # Measure standard jsonschema.validate call
        start_uncompiled = time.perf_counter()
        for _ in range(iterations):
            jsonschema.validate(instance=sample_data, schema=pipeline.schema)
        uncompiled_time = time.perf_counter() - start_uncompiled

        # Measure compiled validator call
        start_compiled = time.perf_counter()
        for _ in range(iterations):
            pipeline._validate_output(sample_data, "gem1")
        compiled_time = time.perf_counter() - start_compiled

        speedup = uncompiled_time / compiled_time if compiled_time > 0 else 0.0

        print("=== Benchmark JSON Schema Validation ===")
        print(f"Iterations: {iterations}")
        print(f"Uncompiled jsonschema.validate: {uncompiled_time:.4f}s ({uncompiled_time / iterations * 1000:.4f} ms/op)")
        print(f"Compiled self.validator.validate: {compiled_time:.4f}s ({compiled_time / iterations * 1000:.4f} ms/op)")
        print(f"Speedup: {speedup:.2f}x faster")


if __name__ == "__main__":
    benchmark_schema_validation()
