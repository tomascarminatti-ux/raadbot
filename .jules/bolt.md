## 2026-06-11 - [Lazy Asyncio Lock Initialization]
**Learning:** In Python 3.10+, creating an `asyncio.Lock` at the module level when no event loop is running (e.g., during import) can lead to `RuntimeError`.
**Action:** Always initialize `asyncio.Lock` lazily inside an asynchronous context (e.g., `if _lock is None: _lock = asyncio.Lock()`).

## 2026-06-11 - [Parallel candidate processing speedup]
**Learning:** Parallelizing candidate processing in the orchestrator using `asyncio.gather` and offloading blocking LLM/IO calls to `asyncio.to_thread` provides a near-linear speedup (measured ~4.86x for 5 candidates).
**Action:** Use `asyncio.gather` for independent sub-tasks in pipelines and ensure thread-safety with locks for shared resource writes.
