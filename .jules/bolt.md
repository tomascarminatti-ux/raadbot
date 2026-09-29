## 2026-03-30 - Prompt Template LRU Caching with File Modification Timestamp Invalidation

**Learning:** Prompt template building in `agent/prompt_builder.py` opens and reads markdown prompt templates from disk on every call. By wrapping file loading in `@functools.lru_cache(maxsize=32)` keyed on filepath and `os.path.getmtime`, disk I/O is eliminated for unchanged prompt files while guaranteeing cache invalidation when prompts are updated on disk. Combining this with pre-compiled module-level regular expressions (`VAR_RE` and `JSON_BLOCK_RE`) resulted in a >3.1x speedup (4,331 ops/sec -> 13,464 ops/sec).

**Action:** Apply `mtime`-based LRU caching for static/template asset file readers and pre-compile regular expressions at module level to eliminate redundant file reads and regex compilation overhead in high-frequency execution loops.
