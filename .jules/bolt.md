## 2026-06-24 - Parallel Candidate Processing in GEM6
**Learning:** Sequential processing of independent entities (candidates) in an orchestrator loop is a significant bottleneck, especially when each entity involves multiple high-latency LLM calls. Even with synchronous LLM clients, offloading to threads and using asyncio concurrency can yield multi-fold speedups.
**Action:** Use `asyncio.gather` with a semaphore to parallelize independent pipeline runs, and wrap synchronous blocking I/O (like LLM calls) in `asyncio.to_thread`.

## 2026-06-24 - Async Safety in Orchestrators
**Learning:** When parallelizing an orchestrator, ensure that shared resources (like a DB client or a logger) are either thread-safe or properly awaited in the main event loop. Using `asyncio.to_thread` for the specific blocking call while keeping the rest of the orchestration logic in the main loop is a clean way to gain performance without massive refactoring.
**Action:** Isolate blocking calls and offload them specifically, rather than trying to make the entire orchestrator "thread-heavy".
