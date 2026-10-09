# Bolt's Journal - Critical Performance Learnings

## 2026-10-09 - Prompt Template Disk I/O Caching with Automatic MTime Invalidation
**Learning:** Frequent template reads from disk (e.g. `load_prompt`, `load_maestro`, `build_prompt`) create repetitive disk I/O overhead. Using `@functools.lru_cache` on a helper function accepting `(filepath, mtime)` avoids unnecessary file reads while automatically invalidating cache when templates are edited on disk without requiring manual cache clearing.
**Action:** Apply `_load_file_cached(filepath, mtime)` with `@functools.lru_cache` whenever reading local template or schema files that are read frequently but modified infrequently.
