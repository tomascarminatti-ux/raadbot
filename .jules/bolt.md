# Bolt's Journal

## 2025-02-22 - Pre-compiled Regexes and Prompt Template LRU Caching
**Learning:** In LLM pipelines that parse raw text responses and load template prompts repeatedly, uncompiled regular expressions and redundant disk I/O on template files create significant execution overhead (~6.7x slower prompt loading). Using `@functools.lru_cache` with file modification timestamp (`mtime`) invalidation along with module-level pre-compiled regex constants (`re.compile`) eliminates I/O and compilation bottlenecks cleanly without sacrificing code readability.
**Action:** Always pre-compile regexes at module level for high-frequency response parsers and wrap disk template loaders in mtime-aware LRU cache helpers.
