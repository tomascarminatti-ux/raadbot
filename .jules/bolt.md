## 2025-05-22 - Parallel Candidate Processing in GEM 6

**Learning:** Sequential processing in the GEM 6 orchestrator created a linear O(N) latency bottleneck where N is the number of candidates. Additionally, shared resources like `pipeline_state.json` in `utils/ws_logger.py` and synchronous LLM calls (`run_gem`) were hidden blockers that would have neutralized parallelization efforts or caused race conditions if not addressed.

**Action:** When parallelizing agent loops, always:
1. Wrap synchronous I/O or CPU-bound calls (like LLM requests) in `asyncio.to_thread`.
2. Use `asyncio.Lock` to protect shared state files.
3. Use `asyncio.gather` to execute independent candidate tasks concurrently.
