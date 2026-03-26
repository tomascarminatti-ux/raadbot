## 2026-03-26 - [Orchestrator Bottleneck: Sequential API Calls]
**Learning:** Sequential processing of candidate evaluation in the `GEM6Orchestrator` created a linear performance degradation. Refactoring the core engine to support async/await and parallelizing processing with a `Semaphore` significantly reduces latency.
**Action:** Use `asyncio.gather` with concurrency control (`asyncio.Semaphore`) for I/O-bound LLM batch operations. Ensure LLM clients are fully asynchronous to prevent blocking the event loop.
