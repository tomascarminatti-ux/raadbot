# Bolt's Performance Journal

## 2026-09-03 - Prompt Template LRU Caching & Invalidation
**Learning:** System prompt templates stored on disk in `prompts/*.md` are accessed frequently during agent pipeline execution and prompt building. Wrapping `load_prompt()` with `@functools.lru_cache(maxsize=32)` provides a ~200x speedup by serving cached strings directly from memory instead of triggering disk I/O reads on every agent invocation. To prevent stale prompt contents when prompts are updated programmatically (such as via `/api/v1/gems/refine`), exposing and calling `clear_prompt_caches()` (`load_prompt.cache_clear()`) immediately invalidates stale entries.
**Action:** Always pair in-memory function-level caching (`@functools.lru_cache`) on file read operations with an explicit cache-invalidation mechanism in mutation endpoints.
