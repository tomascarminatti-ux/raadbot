## 2025-05-15 - Caching and Single-Pass Templating
**Learning:** Disk I/O and multiple `str.replace` passes in prompt construction are significant bottlenecks. Caching file reads with `lru_cache` and using `re.sub` with a callback for single-pass substitution provides a ~10x speedup. Cache invalidation must cover all dependent cached functions (e.g., both prompt and maestro) to avoid stale data.
**Action:** Always use `lru_cache` for static/semi-static asset loading and prioritize single-pass regex substitution for templating. Ensure all related caches are cleared upon asset updates.
