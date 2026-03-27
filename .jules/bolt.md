
## 2025-05-15 - Connection Pooling in GEMClient
**Learning:** Reusing a persistent httpx.AsyncClient session reduces network overhead by avoiding repeated TCP/TLS handshakes, especially beneficial for high-frequency internal API calls.
**Action:** Always prefer persistent sessions for internal clients managed via application lifecycle (e.g., FastAPI lifespan) to ensure proper initialization and closure.
