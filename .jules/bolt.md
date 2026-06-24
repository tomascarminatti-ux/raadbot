## 2026-06-24 - Parallel Candidate Processing in GEM6
**Learning:** Sequential processing of independent entities (candidates) in an orchestrator loop is a significant bottleneck, especially when each entity involves multiple high-latency LLM calls. Even with synchronous LLM clients, offloading to threads and using asyncio concurrency can yield multi-fold speedups.
**Action:** Use `asyncio.gather` with a semaphore to parallelize independent pipeline runs, and wrap synchronous blocking I/O (like LLM calls) in `asyncio.to_thread`.
