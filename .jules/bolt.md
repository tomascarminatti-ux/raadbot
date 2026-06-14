## 2026-06-14 - Parallel Candidate Processing in GEM6 Orchestrator
**Learning:** Sequential candidate processing in the GEM6 Orchestrator was a significant bottleneck due to the I/O-bound nature of LLM calls and file operations. Parallelizing these tasks using `asyncio.gather` and `asyncio.to_thread` resulted in a ~2.5x speedup for a batch of 5 candidates.
**Action:** When processing independent entities in a pipeline, leverage `asyncio.gather` for parallel execution. Always ensure shared resources (e.g., status log files) are protected by an `asyncio.Lock` when introducing concurrency.
