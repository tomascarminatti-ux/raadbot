## 2025-05-15 - [Disk I/O and Caching Optimizations]
**Learning:** Repetitive disk I/O in the agent pipeline (loading schemas and prompt templates) and redundant state saving significantly impact performance during parallel processing. Schema validation was reading from disk on every GEM execution.
**Action:** Use class-level caching for static assets like JSON schemas and `lru_cache` for template files. Minimize state persistence calls by batching them or removing redundant ones that are naturally followed by another save operation.
