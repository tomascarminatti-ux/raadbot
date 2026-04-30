## 2025-05-15 - Optimized Prompt Construction
**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than multiple `.replace()` calls, reducing latency by over 80%. When caching file-based assets with `lru_cache`, it is essential to implement explicit cache invalidation (`func.cache_clear()`) in API endpoints that modify those files to prevent serving stale data.
**Action:** Always prefer single-pass regex substitution for templating and ensure cache consistency when mixing in-memory caching with persistent storage updates.
