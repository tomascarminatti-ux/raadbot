## 2025-05-14 - Parallel Pipeline Execution
**Learning:** Sequential processing of candidates using LLMs is a major bottleneck in talent scraping pipelines. Transitioning to an asynchronous architecture allows for concurrent I/O-bound API calls, significantly improving throughput without sacrificing code readability.
**Action:** Use `asyncio.gather` in orchestrators and ensure LLM clients are fully asynchronous (`async/await`) using libraries like `httpx.AsyncClient` and provider-specific async SDKs.
