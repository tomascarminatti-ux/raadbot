# Bolt's Performance Journal

## 2026-03-30 - Cache File Reads with Modification Timestamp Invalidation
**Learning:** Using `@functools.lru_cache` keyed on `(filepath, mtime)` avoids repetitive disk I/O when reading prompt template files without stale cache risks when prompt files are edited at runtime (e.g. prompt refinement API).
**Action:** Always include file modification time (`os.path.getmtime(filepath)`) as a parameter to cached file loader functions when on-disk changes can occur dynamically.
