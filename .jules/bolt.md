## 2025-05-25 - [Orchestrator Concurrency]
**Learning:** Sequential processing of candidates in `GEM6Orchestrator.run_pipeline` was a major bottleneck, as each candidate's processing is I/O-bound (LLM calls). Additionally, synchronous LLM calls were blocking the event loop, preventing true concurrency.
**Action:** Implemented `asyncio.gather` for parallel candidate processing and `asyncio.to_thread` to offload synchronous LLM calls. This resulted in a ~3.2x speedup for 4 candidates (from 2.20s to 0.69s in benchmark).
