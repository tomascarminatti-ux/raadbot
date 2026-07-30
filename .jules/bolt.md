# Bolt's Performance Optimization Journal

## 2026-07-30 - Prompt Caching & Contract Loading Optimization
**Learning:** High-frequency, repetitive operations in AI pipelines (such as prompt template injection and schema contract validation) are often gated by slow disk I/O and JSON parsing overheads. Applying a thread-safe, in-memory Cache layer (`functools.lru_cache`) drastically improves latency.
When templates are dynamic or programmatically updated (e.g., via a refinement endpoint), cache invalidation must be implemented with precision (`load_prompt.cache_clear()`) to avoid serving stale content.
**Action:** Always identify disk reads and parsing routines in high-frequency loops, cache them using simple in-memory LRU layers, and ensure proper invalidation when mutating those files on disk.
