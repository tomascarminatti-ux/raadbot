# Bolt's Performance Journal

## 2026-11-02 - Cache contract schema loading with mtime invalidation in validate_contract
**Learning:** During multi-agent or multi-candidate pipeline execution, `validate_contract` in `utils/gem_core.py` repeatedly re-reads JSON schema contract files from disk and re-parses them using `json.load`. Decorating contract schema loading with `@functools.lru_cache(maxsize=32)` keyed on `(contract_path, mtime)` eliminates redundant disk I/O and JSON parsing while safely invalidating the cache whenever the contract file timestamp changes on disk. This achieves a ~7.7x validation speedup (from ~26k ops/sec to ~202k ops/sec).
**Action:** When validating data structures or schemas across iterative loops or autonomous agent steps, use in-memory caching with filesystem `mtime` invalidation rather than reading static or semi-static contract files from disk on every invocation.
