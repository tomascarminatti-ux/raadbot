## 2025-05-14 - HTTP Session Reuse for Database API
**Learning:** Reusing a persistent `httpx.AsyncClient` session for internal database API calls in the GEM framework reduced session management overhead by ~88% in local benchmarks (from ~38ms to ~4ms per request). Creating and closing a new client for every request is a significant bottleneck in high-frequency multi-agent pipelines.
**Action:** Always favor dependency injection for `httpx.AsyncClient` or similar network clients to ensure connection pooling. Use the FastAPI `lifespan` pattern to manage shared resource lifecycles.
