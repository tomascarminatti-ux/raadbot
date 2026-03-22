## 2025-05-15 - [Memoization of Template Loading]
**Learning:** Frequent disk I/O for loading prompt templates was a significant bottleneck during high-volume or parallel pipeline execution. Using `functools.lru_cache` on file loading functions significantly reduces latency by eliminating redundant disk reads.
**Action:** Always consider memoization for read-only configuration or template files that are accessed multiple times during a single execution flow.
