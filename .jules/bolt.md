## 2026-04-29 - Prompt Building Optimization
**Learning:** Redundant disk I/O and regex compilation in high-frequency functions like `build_prompt` can be easily mitigated with `lru_cache` and module-level pre-compilation, but cache invalidation must be explicitly handled in API endpoints that modify the source files.
**Action:** Always verify if a cached resource can be updated via the API and add `cache_clear()` calls in the corresponding write paths.
