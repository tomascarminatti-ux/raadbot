## 2026-06-20 - Parallel Orchestration & Template Caching
**Learning:** Sequential processing of candidates in the orchestrator was a major bottleneck (O(n) where n is candidate count * LLM latency). Additionally, repeated disk I/O for prompt templates added unnecessary micro-latency and overhead.
**Action:** Use `asyncio.gather` for parallel agent execution and `asyncio.to_thread` to offload blocking LLM/IO calls from the event loop. Implement `lru_cache` for static template loading to eliminate redundant disk reads.
