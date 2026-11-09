# Bolt's Journal - Critical Performance Learnings

## 2025-05-18 - File-based prompt template caching with automatic invalidation
**Learning:** Disk I/O on static template files (`prompts/*.md`) executed repeatedly inside iterative loops (e.g., across multiple candidates and GEM stages) creates unnecessary latency (>4x slowdown on file reads). Naive caching without invalidation risks serving stale prompt templates if prompt files are updated during runtime. Keying `@functools.lru_cache` by `(filepath, mtime)` provides zero-cost in-memory prompt reuse while guaranteeing immediate cache invalidation when a template is modified on disk.
**Action:** When caching file reads in Python services without an external cache service, use `_cached_reader(filepath, os.path.getmtime(filepath))` wrapped with `@functools.lru_cache(maxsize=...)` for safe, self-invalidating in-memory caching.
