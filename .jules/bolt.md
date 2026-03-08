## 2026-03-08 - Parallel Orchestration with Async Gemini Client
**Learning:** Sequential processing of candidates in the orchestrator was a major bottleneck ($O(N)$ latency). Transitioning the LLM client to `asyncio` and using `asyncio.gather` in the orchestrator allows concurrent processing, reducing batch latency by ~89% in benchmarks.
**Action:** Always prefer asynchronous LLM clients and concurrent processing for batch operations or independent agent tasks. Ensure all call sites are properly updated to `await` and that testing covers the new async flow.
