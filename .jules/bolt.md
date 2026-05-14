## 2025-05-14 - Asynchronous LLM calls and parallel candidate processing
**Learning:** Sequential processing of candidates and synchronous LLM calls are a major bottleneck. Moving to an async client with `asyncio.gather` and a semaphore significantly improves throughput.
**Action:** Use `httpx.AsyncClient` and `asyncio.gather` with `Semaphore` for all I/O-bound operations in pipelines.
