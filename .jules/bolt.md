# Bolt's Journal - Critical Learnings

## 2026-03-05 - File Modification Time (mtime) Caching Pattern
**Learning:** In a multi-agent application with frequent file read operations (such as loading prompts and JSON schemas), naive file reading causes significant disk I/O overhead. Standard `lru_cache` can cause stale data when prompts or schemas are modified dynamically. Using file modification time (`mtime`) as a parameter to the cached loading helper ensures safe cache invalidation on disk modifications without needing manual cache clearing logic.
**Action:** Always wrap file loading utilities in an `mtime`-based cache decorator (`@functools.lru_cache`) to dynamically invalidate the cache whenever a file's timestamp updates.
