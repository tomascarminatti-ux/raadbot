## 2024-05-15 - [Persistent httpx Session in GEMClient]
**Learning:** Reusing a persistent `httpx.AsyncClient` session for successive API calls significantly reduces overhead from TCP/TLS handshakes, especially when interacting with a local or sidecar database service.
**Action:** Always prefer persistent sessions for internal API clients that make multiple requests during a single task or pipeline execution. Ensure proper resource cleanup by implementing an `aclose()` method and using `try...finally` in the caller.
