# Bolt's Journal - Critical Performance Learnings

## 2026-10-08 - Contract loading caching in `validate_contract`
**Learning:** In step-by-step orchestration (such as `GEM6Orchestrator`), `validate_contract` reads JSON contract schemas from disk on every validation call. Caching `json.load` calls using `@functools.lru_cache` keyed by file path and `os.path.getmtime` modification timestamp eliminates disk I/O while automatically invalidating the cache when schema files are modified on disk. This provided a ~7.5x performance speedup (from 0.0372 ms/call down to 0.0051 ms/call).
**Action:** When validating data against disk-based schema files or configs, cache the parsed content using `os.path.getmtime` as part of the LRU cache key for zero-overhead cache invalidation.
