## 2026-07-22 - Prompt Caching Cache Invalidation
**Learning:** In environments where users can dynamically refine system prompt templates via an API, caching compiled templates in-memory with `lru_cache` introduces a major risk of stale templates being used for subsequent pipeline runs.
**Action:** Always export a cache invalidation helper (e.g. `clear_prompt_caches()`) and invoke it inside the API endpoint immediately after writing any newly refined templates to disk to ensure consistency.
