import time
import os
import sys
import json

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient
from unittest.mock import MagicMock

def benchmark():
    mock_gemini = MagicMock(spec=GeminiClient)
    output_dir = "runs/test_bench/outputs"
    os.makedirs(output_dir, exist_ok=True)

    # Instance creation overhead (includes loading schema from disk)
    start_init = time.perf_counter()
    for _ in range(100):
        pipeline = Pipeline(mock_gemini, "SEARCH-2024-001", output_dir)
    end_init = time.perf_counter()
    print(f"Average Pipeline.__init__ time (loads schema): {(end_init - start_init)/100 * 1000:.4f}ms")

    pipeline = Pipeline(mock_gemini, "SEARCH-2024-001", output_dir)

    sample_output = {
        "meta": {
            "search_id": "SEARCH-2024-001",
            "gem": "GEM_1",
            "prompt_version": "v1.0",
            "timestamp": "2024-01-01T00:00:00Z",
            "sources": ["source1"]
        },
        "scores": {"confidence": 5, "score_dimension": 8},
        "blockers": [],
        "content": {}
    }

    # Warmup
    pipeline._validate_output(sample_output, "gem1")

    iterations = 1000
    start_val = time.perf_counter()
    for _ in range(iterations):
        pipeline._validate_output(sample_output, "gem1")
    end_val = time.perf_counter()

    avg_val = ((end_val - start_val) / iterations) * 1000
    print(f"Average _validate_output time: {avg_val:.4f}ms")

if __name__ == "__main__":
    benchmark()
