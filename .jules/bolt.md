## 2026-03-07 - Parallel Candidate Processing with Async Gemini Client
**Learning:** Sequential processing of multiple entities (candidates) in an LLM-driven pipeline creates a massive bottleneck when LLM latency is ~2-5s per call. Batch processing using `asyncio.gather` can reduce total latency by nearly N times (where N is the number of candidates), provided the provider limits aren't hit.
**Action:** Always prefer asynchronous LLM clients and parallelize entity processing in the orchestrator to ensure scalability and better user experience.
