
import time
import os
import sys
import asyncio
from typing import Dict, Any, Optional

# Add current directory to path so we can import agent modules
sys.path.append(os.getcwd())

from agent.prompt_builder import build_prompt, load_prompt
from agent.gemini_client import GeminiClient, GeminiResult
from agent.gem6.orchestrator import GEM6Orchestrator

class MockGeminiClient:
    async def run_gem(self, prompt: str, gem_name: Optional[str] = None, max_retries: int = 0) -> Dict[str, Any]:
        await asyncio.sleep(0.1) # Simulate network delay
        return {
            "json": {"action": "finalize", "status": "SUCCESS", "thought": "Done"},
            "markdown": "Done",
            "raw": "Done",
            "usage": {"total_tokens": 100}
        }

async def benchmark_prompt_builder():
    print("Benchmarking prompt_builder.py...")
    start_time = time.time()
    iterations = 100
    for i in range(iterations):
        build_prompt("gem5", {"input": {"test": "data"}})

    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average time for build_prompt: {avg_time*1000:.4f} ms")

async def benchmark_gemini_client_parsing():
    print("Benchmarking gemini_client.py parsing...")
    client = GeminiClient(api_key="dummy")

    raw_text = """
    Here is some analysis.
    ```json
    {
      "key": "value",
      "list": [1, 2, 3]
    }
    ```
    More text.
    """

    start_time = time.time()
    iterations = 1000
    for i in range(iterations):
        client._parse_response(raw_text)

    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average time for _parse_response: {avg_time*1000:.4f} ms")

async def benchmark_orchestrator_parallel():
    print("Benchmarking orchestrator parallel processing...")
    mock_client = MockGeminiClient()

    # We need to mock the DB client too to avoid connection errors
    orchestrator = GEM6Orchestrator(gemini=mock_client)
    # Monkeypatch the db client to be a no-op
    class MockDB:
        async def log_execution(self, *args, **kwargs): pass
        async def upsert_entity(self, *args, **kwargs): pass
    orchestrator.client = MockDB()

    # Mock search inputs and candidates
    search_inputs = {"role": "test"}
    num_candidates = 10
    candidates = {f"CAND-{i}": {"data": f"test-{i}"} for i in range(num_candidates)}

    start_time = time.time()
    await orchestrator.run_pipeline(search_inputs, candidates)
    end_time = time.time()

    duration = end_time - start_time
    print(f"Time for {num_candidates} candidates: {duration:.4f} s")
    return duration

async def main():
    await benchmark_prompt_builder()
    await benchmark_gemini_client_parsing()
    await benchmark_orchestrator_parallel()

if __name__ == "__main__":
    asyncio.run(main())
