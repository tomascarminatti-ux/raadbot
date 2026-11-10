# Bolt's Performance Journal

## 2026-04-16 - Reusable HTTP client sessions vs per-call instantiation in async orchestrators
**Learning:** Instantiating `httpx.AsyncClient` inside every method call (`async with httpx.AsyncClient() as client:`) introduces substantial overhead (~30ms+ per call) due to repeated event loop binding, transport setup, and SSL/connection pool teardown. In multi-agent loops where hundreds of entities and logs are processed, persistent client pooling reduces dispatch latency by >100x.
**Action:** Always maintain a lazily initialized persistent `httpx.AsyncClient` on client classes with an explicit `close()` cleanup and async context manager methods (`__aenter__`/`__aexit__`).

## 2026-04-16 - Pytest testpaths restriction and standalone script isolation
**Learning:** In CI workflows running `pytest` without path arguments, pytest discovers any root-level file starting with `test_` (like `test_gemini.py`). When top-level code in such scripts executes live HTTP or provider requests without `__name__ == '__main__'`, CI fails with collection errors.
**Action:** Always configure `testpaths = tests` in `pytest.ini` and guard root-level demonstration/utility scripts with `if __name__ == '__main__':`.
