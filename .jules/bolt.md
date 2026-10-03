# Bolt Journal ⚡

## 2026-02-25 - Prompt Template LRU Caching with mtime Invalidation
**Learning:** In LLM pipelines and prompt builders, repeated loading of prompt markdown templates from disk adds I/O overhead. Decorating a file reader function with `@functools.lru_cache(maxsize=32)` using the file modification timestamp (`os.path.getmtime`) as part of the cache key achieves significant speedups (~3x - 6x) while preserving automatic cache invalidation whenever prompt files are modified on disk.
**Action:** Use `mtime`-backed `@functools.lru_cache` for configuration, prompt templates, or JSON schemas that are read frequently from disk during API request cycles.
