## 2026-03-31 - Cache Prompt Template Loading with mtime Invalidation & Pre-compiled Regex

**Learning:** Prompt templates are frequently read from disk and parsed for variable placeholders (`{{variable}}`) across pipeline executions. Combining `@functools.lru_cache(maxsize=32)` on file modification timestamp (`mtime`) with pre-compiled module-level regex (`VAR_RE`) eliminates disk I/O and regex compilation overhead without risking stale content when prompt files are modified on disk.

**Action:** Wrap file-loading helpers with an LRU cache taking `(filepath, mtime)` as arguments, and pre-compile template extraction regex at module level.
