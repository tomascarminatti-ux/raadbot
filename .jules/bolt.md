## 2026-02-25 - LRU Caching Prompt Files with File Timestamp Invalidation
**Learning:** In prompt builder pipelines where templates are loaded repeatedly, wrapping file reads with `@functools.lru_cache` keyed by file path and `mtime` (`os.path.getmtime(filepath)`) avoids disk I/O on repeated calls while ensuring immediate cache invalidation when prompt files are modified on disk.
**Action:** Use `mtime`-keyed LRU caching for static or infrequently modified filesystem template loaders to achieve multi-fold speedups without stale reads.
