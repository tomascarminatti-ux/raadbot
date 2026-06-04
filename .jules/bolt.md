## 2026-06-04 - [Parallel Candidate Processing]
**Learning:** Sequential processing of candidates in GEM6Orchestrator caused a linear increase in total execution time. Using `asyncio.gather` combined with `asyncio.to_thread` for synchronous LLM calls allowed for true concurrent processing of candidates.
**Action:** Always prefer `asyncio.gather` for processing independent entities and ensure synchronous I/O or API calls are offloaded to threads using `asyncio.to_thread` when working within an async event loop.
