# Bolt Agent Journal - Critical Learnings Only

## 2026-03-05 - File system I/O bottleneck in Agent prompting
**Learning:** In highly orchestrative/stateful multi-agent workflows (such as GEM6 processing up to 10 iterations per candidate), prompt template files and schema JSON files are repeatedly loaded from disk. This results in significant redundant file system overhead and read-latency.
**Action:** Implement memory caching (`functools.lru_cache`) for loaded templates and json schemas, ensuring appropriate cache invalidation APIs exist when templates are refined programmatically.
