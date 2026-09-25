# Bolt's Performance Journal

## 2026-03-31 - Prompt Template LRU Caching with mtime Invalidation
**Learning:** Reading prompt templates synchronously from disk on every `build_prompt` call adds repetitive I/O overhead. Caching prompt files with `@functools.lru_cache` keyed on `(filepath, mtime)` avoids redundant disk reads while automatically invalidating if prompt files are modified on disk.
**Action:** Use `@functools.lru_cache(maxsize=32)` with `os.path.getmtime` for filesystem template and schema reads.
