# Bolt's Journal - Critical Learnings

## 2026-03-30 - Prompt Template LRU Caching with Mtime Invalidation
**Learning:** Decorating file loader functions with `@functools.lru_cache(maxsize=32)` keyed by `(filepath, mtime)` avoids repetitive disk I/O on prompt templates during multi-candidate pipeline iterations, providing a ~3.3x speedup. When unit testing mtime invalidation with `os.utime`, `os.utime` must be called *after* `write_text()` to prevent `write_text()` from resetting the modification timestamp to system time.
**Action:** Use `(filepath, mtime)` keys for file caching and ensure `os.utime` call occurs after file writes in unit tests.
