# Bolt Performance Journal

## 2026-05-18 - Thread-safe background persistence for logs
**Learning:** Offloading synchronous file I/O (like `json.dump`) to a background thread using `asyncio.to_thread` in an `async` application can lead to `RuntimeError: list changed size during iteration` if the main thread modifies the data structure during serialization.
**Action:** Always take a shallow or deep snapshot of the data structure (e.g., `list(data)`) within a lock before passing it to the background thread for serialization.

## 2026-05-18 - Parallel Orchestration with GEM 6
**Learning:** Sequential processing of candidates in a multi-agent orchestrator is a massive bottleneck. `asyncio.gather` combined with `asyncio.to_thread` for blocking LLM calls allows for true parallelism and significantly reduces total execution time.
**Action:** Refactor sequential loops that contain blocking I/O or network calls to use `asyncio.gather` and `asyncio.to_thread`.
