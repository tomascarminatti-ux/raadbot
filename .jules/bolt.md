## 2026-06-07 - Parallel Orchestration with Thread Offloading
**Learning:** Sequential processing of multiple candidates is a major bottleneck in I/O-bound LLM pipelines. Synchronous LLM clients (like GeminiClient here) can block the entire event loop if not properly offloaded, even when using asyncio.
**Action:** Always use `asyncio.gather` for independent tasks and `asyncio.to_thread` for blocking synchronous calls within an async context to maintain true concurrency.
