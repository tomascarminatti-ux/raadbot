## 2025-05-22 - Prompt Template Caching
**Learning:** Disk I/O for reading prompt templates is a significant bottleneck in agentic loops. Caching these with `lru_cache` provides a measurable speedup (~58% in this case).
**Action:** Always use `lru_cache` for file-based configuration or template loaders, but remember to clear the cache when the underlying files are updated (e.g., via refinement endpoints).
