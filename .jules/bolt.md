# Bolt Journal - Performance Learnings

## 2026-06-17 - Parallelizing Orchestration and Thread Offloading
**Learning:** Sequential processing of candidates in an LLM-based orchestrator creates a linear bottleneck. Since LLM calls and file I/O are I/O-bound, using `asyncio.gather` for parallel candidate processing significantly reduces total execution time. Additionally, offloading blocking synchronous calls (like `gemini.run_gem` and local file I/O) to worker threads using `asyncio.to_thread` prevents event loop starvation, allowing true concurrency.
**Action:** Always check for sequential loops over independent items (like candidates or sources) and parallelize them. Ensure synchronous library calls in async methods are properly offloaded to threads.
