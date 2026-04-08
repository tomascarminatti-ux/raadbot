## 2025-04-08 - [Persistent Session Optimization]
**Learning:** Reusing a persistent `httpx.AsyncClient` session for internal API calls (like to a database service) significantly reduces latency by avoiding repeated TCP/TLS handshakes. In this local benchmark, latency dropped from ~60ms to ~5ms per call.
**Action:** Always prefer persistent sessions for internal microservice communication within the same pipeline execution. Ensure proper cleanup using `aclose()` and `try...finally` blocks.
