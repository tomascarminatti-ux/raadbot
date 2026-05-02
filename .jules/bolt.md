## 2025-05-14 - Efficient Template Substitution
**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than nested loops or multiple `.replace()` calls, especially as the number of variables or the template size increases. It reduces complexity from O(M*N) to O(N).
**Action:** Prefer single-pass substitution with regex callbacks for templating logic.

## 2025-05-14 - Disk I/O Caching for Static Assets
**Learning:** Static assets like prompt templates are frequently accessed but rarely changed. Caching them with `lru_cache` significantly reduces disk I/O latency.
**Action:** Implement `lru_cache` for disk-read operations on static assets and ensure explicit cache invalidation (`cache_clear`) in update paths.
