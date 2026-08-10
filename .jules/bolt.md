# Bolt's Journal

## 2026-03-05 - [MTime-Based Cache Invalidation for Dynamic Prompt Templates and Data Contracts]
**Learning:** In a highly interactive multi-agent system, template files (e.g., prompt system templates) and schema files are prone to runtime modifications (such as programmatic refinement via `/api/v1/gems/refine` or dynamic schemas generated during test suites). Applying a standard `functools.lru_cache` directly leads to stale data and subtle bugs.
By incorporating the file's modification timestamp (`mtime`) directly as an additional argument to the cached helper function, Python's built-in `lru_cache` automatically handles precise invalidation on disk updates without requiring manual cache-clearing mechanisms or complex tracking logic.
**Action:** Always combine `functools.lru_cache` with a file modification timestamp helper `os.path.getmtime()` when caching filesystem resources that can be modified during application or test lifecycles.
