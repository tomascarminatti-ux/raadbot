## 2025-05-15 - [Prompt Template Caching & Invalidation]
**Learning:** Adding `@lru_cache` to file-loading functions (like `load_prompt`) significantly reduces disk I/O, but it creates a consistency risk if those files can be updated at runtime (e.g., via a refinement API).
**Action:** Always pair file-loading caches with explicit `.cache_clear()` calls in the write-paths of those files to ensure the application doesn't serve stale data.
