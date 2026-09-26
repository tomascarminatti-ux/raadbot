# Bolt's Performance Journal

## 2026-03-30 - Caching Prompt Template Reads with LRU and mtime Invalidation
**Learning:** Prompt template markdown files are read repeatedly from disk during agent orchestration steps. Decorating a helper reader function with `@functools.lru_cache(maxsize=32)` using file modification timestamp (`mtime`) as a cache key eliminates disk I/O on repeated calls while guaranteeing immediate cache invalidation when prompt files are refined or edited on disk. Pre-compiling module-level regex objects further reduces parsing overhead.
**Action:** Use `@functools.lru_cache` with `os.path.getmtime` for file-based template/schema readers and module-level pre-compiled regex constants for high-frequency text parsing.
