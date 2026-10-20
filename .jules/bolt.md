# Bolt's Journal - Critical Performance Learnings

## 2025-05-18 - JSON Contract Loading Optimization with LRU Cache
**Learning:** In multi-step agent pipeline orchestration (such as GEM 6 step iterations), repeated contract schema validation reads JSON contract definition files from disk on every step. Caching contract schema loading using `@functools.lru_cache` keyed by file path and modification timestamp (`mtime`) eliminates disk I/O overhead without risking stale schema cache when schema files are edited.
**Action:** When validating against file-based schema definitions or contracts in tight execution loops, wrap file reading in an `@lru_cache` helper taking `(filepath, os.path.getmtime(filepath))`.
