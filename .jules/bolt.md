
## 2026-04-17 - [Connection Pooling and Template Caching]
**Learning:**  was creating a new  for every request, which added significant overhead (~65ms per call) due to TCP/TLS handshakes. Refactoring to a persistent client with lazy initialization reduced latency to ~3ms. Additionally, redundant disk I/O for prompt templates was solved by applying `@lru_cache` to `load_prompt`.
**Action:** Always implement connection pooling for internal API clients and cache static assets like prompt templates in memory.

## 2026-04-17 - [Connection Pooling and Template Caching]
**Learning:** GEMClient was creating a new httpx.AsyncClient for every request, which added significant overhead (~65ms per call) due to TCP/TLS handshakes. Refactoring to a persistent client with lazy initialization reduced latency to ~3ms. Additionally, redundant disk I/O for prompt templates was solved by applying `@lru_cache` to `load_prompt`.
**Action:** Always implement connection pooling for internal API clients and cache static assets like prompt templates in memory.
