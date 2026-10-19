# Bolt's Journal - Critical Learnings

## 2024-05-15 - Prompt Template Loading & Regex Pre-compilation
**Learning:** Re-reading markdown prompt template files on every Gemini request introduced unnecessary file I/O overhead. Decorating a file loading helper with `@functools.lru_cache(maxsize=32)` using `filepath` and `mtime` as cache keys achieves >4x speedup in prompt template loading while ensuring automatic cache invalidation whenever prompt files are modified on disk. Additionally, pre-compiling regexes (`VAR_RE`, `JSON_BLOCK_RE`) as module-level constants eliminates string-to-regex compilation overhead across pipeline runs.
**Action:** Always combine `lru_cache` with `mtime` checks when caching disk file reads, and pre-compile regular expressions used in hot loops or response parsers.
