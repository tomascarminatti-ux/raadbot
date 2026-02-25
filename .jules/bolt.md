## 2025-05-22 - Optimized Prompt Building with Caching and Single-Pass Injection
**Learning:** Prompt building using multiple `.replace()` calls in a loop is O(N*M) and can be a significant bottleneck as templates and the number of variables grow. Additionally, repeated disk I/O for static templates adds unnecessary latency.
**Action:** Use `@functools.lru_cache` for template loading and `re.sub` with a callback for single-pass variable injection. Ensure cache invalidation (`cache_clear()`) is implemented in API endpoints that modify templates.
