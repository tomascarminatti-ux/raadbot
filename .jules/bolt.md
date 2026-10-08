# Bolt's Journal - Critical Performance Learnings

## 2026-03-31 - Template File Loading Optimization with Mtime Invalidation
**Learning:** Prompt templates and schemas read repeatedly during execution loops introduce redundant disk I/O and regex string compilation overhead. Using `@functools.lru_cache` keyed on file path and modification timestamp (`mtime`) eliminates disk reads while guaranteeing automatic cache invalidation when prompt templates are updated on disk.
**Action:** Wrap file-loading helpers in an LRU cache using `os.path.getmtime` as a cache key component, and pre-compile regular expressions as module-level constants.
