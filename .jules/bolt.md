## 2025-05-18 - JSON Contract Validation Caching with mtime
**Learning:** `validate_contract` in `utils/gem_core.py` was reading and parsing schema JSON files from disk on every validation call during orchestration. Decorating the contract loader helper `_load_contract_cached` with `@functools.lru_cache(maxsize=32)` using `os.path.getmtime(contract_path)` eliminates disk I/O and JSON parsing overhead while automatically invalidating the cache when files on disk are updated.
**Action:** Use mtime-keyed LRU caching for static or rarely modified file resources loaded during pipeline execution.
