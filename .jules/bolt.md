## 2026-04-27 - Optimized Prompt Construction
**Learning:** Repetitive disk I/O for static template files and redundant regex compilation in core logic significantly impacts latency in agentic workflows.
**Action:** Always implement caching (e.g., `lru_cache`) for frequently accessed static assets like prompt templates and ensure corresponding cache invalidation (e.g., `func.cache_clear()`) in API endpoints that update those assets on disk. Pre-compile regex patterns used in high-frequency loops.
