# Bolt's Journal - Performance Learnings

## 2026-09-28 - File modification timestamp (mtime) caching for prompt templates
**Learning:** Dynamic prompt templates stored on disk can cause repetitive I/O overhead when loaded inside iterative agent execution loops. Decorating the loading function with `@functools.lru_cache` keyed by file path and `mtime` (`os.path.getmtime`) avoids disk reads on repeated template builds while ensuring instant cache invalidation when prompts are modified (e.g. via prompt refinement API endpoints). Pre-compiling variable replacement regexes at the module level yields further CPU savings, providing a >16x speedup (~0.137ms down to ~0.008ms per load).
**Action:** Always key file cache helpers with `os.path.getmtime` for filesystem resources that may be mutated during runtime.
