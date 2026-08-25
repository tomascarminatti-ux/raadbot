## 2026-08-25 - Prompt Template LRU Caching
**Learning:** Adding `@functools.lru_cache(maxsize=32)` to `load_prompt()` and pre-compiling prompt variable regex (`VAR_RE`) eliminates disk I/O and regex parsing overhead during prompt construction, yielding a ~14.6x speedup. Proper invalidation must be wired to endpoint functions (`clear_prompt_caches()` in `api.py`) whenever templates are updated.
**Action:** Always check for disk-read loops in template/prompt loading logic and apply LRU caching with explicit invalidation triggers on mutation.
