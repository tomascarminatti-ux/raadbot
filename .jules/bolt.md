## 2024-05-11 - Optimized prompt construction with caching and regex
**Learning:** Repeated disk I/O for loading templates and iterative `str.replace` calls for variable injection in a hot path (LLM prompt construction) can significantly degrade performance, especially when orchestrated at scale.
**Action:** Use `@lru_cache` for template loading and pre-compiled regex with `re.sub` for single-pass variable replacement. Always ensure cache invalidation when templates are modified.
