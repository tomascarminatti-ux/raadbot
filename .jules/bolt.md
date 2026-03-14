## 2026-03-14 - Prompt Loading Optimization
**Learning:** Reading prompt templates from disk for every agent call becomes a measurable bottleneck in batch-processing pipelines (e.g., Hub-and-Spoke 3.0). Caching these strings in memory significantly reduces latency.
**Action:** Implement `@functools.lru_cache` for prompt loading functions to eliminate redundant I/O.
