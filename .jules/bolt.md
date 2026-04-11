## 2025-05-14 - HTTP Connection Pooling for DB API
**Learning:** Reusing an `httpx.AsyncClient` instance instead of creating a new one for each request significantly reduces latency (from ~43ms to ~3ms) by enabling TCP/TLS connection pooling.
**Action:** Always prefer persistent clients for internal service communication and ensure proper `aclose()` lifecycle management.
