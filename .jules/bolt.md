# Bolt's Journal - Critical Learnings

## 2026-03-30 - [Mtime-based Cache Invalidation for File Loading]
**Learning:** In a performance-obsessed pipeline executing repeatedly, reading files (prompts and JSON contracts) from disk is a massive bottleneck. However, typical `lru_cache` on functions reading from disk is prone to stale-cache bugs if the files are modified during runtime (such as in tests or endpoint operations). Using `os.path.getmtime(filepath)` inside the wrapper and passing it as an argument to the `@lru_cache` helper completely resolves this issue. The cache key becomes `(filepath, mtime)`, meaning files are loaded from cache at memory speeds, but automatically invalidate/reload the instant a file is modified on disk.
**Action:** Always use `mtime`-based parameters for caching functions that read local filesystem content that can occasionally be modified.
