# Bolt Performance Journal

## 2026-02-25 - Prompt Template LRU Caching with MTime Invalidation
**Learning:** Calling template resolution functions like `load_prompt` repeatedly during pipeline orchestration causes excessive disk I/O. Using `@functools.lru_cache(maxsize=32)` on a helper keyed on `(filepath, mtime)` avoids redundant file reads while ensuring automatic cache invalidation when prompt files are modified on disk (e.g., via user prompt refinement). Pre-compiling `VAR_RE` regex further eliminates string compilation overhead.
**Action:** When caching file reads in Python applications, use `mtime = os.path.getmtime(path)` as a cache key argument to `lru_cache` to combine zero-overhead memory reads with instant disk invalidation upon file updates.
