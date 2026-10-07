# Bolt's Journal - Critical Performance Learnings

## 2026-02-25 - httpx.AsyncClient Session Reuse vs Per-Request Instantiation
**Learning:** Instantiating a new `httpx.AsyncClient()` on every async HTTP request creates ~35ms of overhead per call due to repeated connection pool and transport initialization. Reusing a persistent `AsyncClient` instance reduces call time to ~0.3ms (~108x speedup) by preserving connection pools.
**Action:** Always maintain a persistent `_client` instance in API client classes with lazy initialization and async context manager (`__aenter__`/`__aexit__`) or `close()` cleanup support.
