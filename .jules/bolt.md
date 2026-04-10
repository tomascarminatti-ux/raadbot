## 2026-04-10 - Connection Pooling & Schema Caching
**Learning:** Initial overhead of creating a new `httpx.AsyncClient` for every DB API call was ~37ms. By moving to a persistent client, this was reduced to ~3ms per call. Schema validation using `json.load` on every call also added unnecessary I/O latency (~0.04ms vs ~0.001ms with caching).
**Action:** Use persistent clients for internal service communication and cache static assets like JSON schemas.
