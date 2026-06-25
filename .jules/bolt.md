## 2026-06-25 - Parallel Orchestration & Async Offloading
**Learning:** Sequential processing of independent entities (candidates) in an orchestration pipeline is a major bottleneck. Synchronous LLM clients (like `google-genai` when not using its async methods) block the event loop, preventing true parallelism even with `asyncio.gather`.
**Action:** Use `asyncio.gather` with `asyncio.Semaphore` for entity parallelism and `asyncio.to_thread` to offload synchronous I/O or LLM calls to worker threads.
