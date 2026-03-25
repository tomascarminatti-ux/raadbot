# Bolt's Performance Journal

## 2026-03-25 - HTTP Connection Pooling in Async Environments
**Learning:** Reusing an `httpx.AsyncClient` session significantly reduces overhead (measured ~88% improvement for 10 calls) in applications performing multiple successive API calls. Creating a new client for each request causes redundant TCP/TLS handshake overhead. In FastAPI, the `lifespan` context manager is the ideal place to manage the lifecycle of such persistent clients.
**Action:** Always prefer persistent sessions for internal API clients. Use FastAPI's `app.state` to store and share these clients across the application.
