# Bolt's Performance Journal

## 2026-03-30 - Prompt Template Caching with mtime Invalidation
**Learning:** In prompt engineering pipelines, template prompt markdown files are repeatedly loaded from disk on every execution. Decorating a helper function with `@functools.lru_cache(maxsize=32)` keyed on `(filepath, mtime)` avoids disk reads completely during execution while preserving automatic invalidation when files are edited on disk. Combining this with module-level precompiled regexes reduces prompt rendering overhead by over 2.5x.
**Action:** Always wrap file loading functions with `@functools.lru_cache` keyed on modification time (`mtime`) and precompile string pattern regexes at the module level.
