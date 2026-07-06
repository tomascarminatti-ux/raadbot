import time
import sys
import os
import asyncio
import json
from unittest.mock import MagicMock

# Add the root directory to sys.path
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt
from agent.pipeline import Pipeline
from agent.gemini_client import GeminiClient

def benchmark_prompt_builder():
    print("--- Benchmarking Prompt Builder ---")
    variables = {
        "search_id": "test-search",
        "candidate_id": "CAND-001",
        "cv_text": "A" * 10000,
        "interview_notes": "B" * 5000,
        "gem5_summary": "C" * 2000,
        "gem5_key_challenge": "D" * 1000
    }

    # Warmup
    for _ in range(10):
        build_prompt("gem1", variables)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        build_prompt("gem1", variables)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Total time for {iterations} iterations: {duration:.4f}s")
    print(f"Average time per iteration: {duration/iterations*1000:.4f}ms")
    return duration / iterations

async def benchmark_schema_loading():
    print("\n--- Benchmarking Schema Loading ---")
    mock_gemini = MagicMock(spec=GeminiClient)
    pipeline = Pipeline(gemini=mock_gemini, search_id="test", output_dir="runs/test")

    # Warmup
    pipeline._load_schema()

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        pipeline._load_schema()
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Total time for {iterations} schema loads: {duration:.4f}s")
    print(f"Average time per load: {duration/iterations*1000:.4f}ms")
    return duration / iterations

def benchmark_json_parsing():
    print("\n--- Benchmarking JSON Parsing (GeminiClient) ---")
    client = GeminiClient(api_key="fake")
    raw_text = "Some markdown\n```json\n" + json.dumps({"key": "value" * 100}) + "\n```\nMore markdown"

    # Warmup
    for _ in range(10):
        client._parse_response(raw_text)

    start_time = time.perf_counter()
    iterations = 1000
    for _ in range(iterations):
        client._parse_response(raw_text)
    end_time = time.perf_counter()

    duration = end_time - start_time
    print(f"Total time for {iterations} JSON parses: {duration:.4f}s")
    print(f"Average time per parse: {duration/iterations*1000:.4f}ms")
    return duration / iterations

async def main():
    benchmark_prompt_builder()
    await benchmark_schema_loading()
    benchmark_json_parsing()

if __name__ == "__main__":
    asyncio.run(main())
