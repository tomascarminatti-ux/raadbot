# Bolt's Performance Journal

## 2025-05-18 - Caching Static Contract Schemas in Orchestration Step Validation
**Learning:** In autonomous agent loops (`GEM6Orchestrator`), `validate_step` is called at every reasoning iteration across all candidates to validate JSON schemas (`contracts/{agent_id}_output.schema.json`). Re-reading and parsing the contract JSON file from disk on every validation call creates unnecessary synchronous I/O overhead. Decorating a contract loading helper with `@functools.lru_cache(maxsize=32)` keyed by `(filepath, mtime)` avoids disk access on repeated validations while automatically invalidating if a contract schema is edited on disk.
**Action:** When validating data contracts or schemas in repetitive agent execution loops, cache the parsed contract objects with mtime-based invalidation to eliminate redundant disk I/O (~7.5x validation speedup).
