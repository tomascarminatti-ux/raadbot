## 2026-02-24 - Blocking I/O in Async Broadcast
**Learning:** The `broadcast_log` function in `utils/ws_logger.py` was performing synchronous disk read/write on every call. In an `async` orchestrator, this blocks the event loop, causing significant latency (~0.66ms per log on local disk, potentially much worse in production).
**Action:** Use in-memory caching for state and offload blocking disk I/O to background threads using `asyncio.to_thread` with proper `threading.Lock` to prevent file corruption.

## 2026-02-24 - Prompt Template Substitution
**Learning:** Sequential `.replace()` calls for multiple variables in large prompt templates are inefficient. Caching templates with `lru_cache` and using a single-pass `re.sub` provides a ~4x speedup.
**Action:** Always cache disk-loaded templates and use single-pass regex substitution for variable injection.
