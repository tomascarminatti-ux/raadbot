# Bolt Journal - Critical Performance learnings

## 2025-06-18 - [Optimizing JSON Contract Validation via LRU Caching]
**Learning:** Frequent filesystem reads and JSON parsing of schema files in `validate_contract` add significant CPU overhead and disk I/O. We can use `@functools.lru_cache(maxsize=32)` to cache loaded JSON schemas. Adding file-modification-time (mtime) as an argument to the cached loading helper ensures safe cache invalidation without stale data issues.
**Action:** Implement `_load_contract_cached(contract_path, mtime)` with LRU cache, and call it inside `validate_contract`.
