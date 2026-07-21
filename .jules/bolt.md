## 2026-03-01 - Prompt and Contract Caching
**Learning:** High-frequency validation and multi-agent pipeline loops repeatedly hit the disk to read JSON contracts and prompt Markdown files. Standard disk I/O operations create substantial latency when scaled to hundreds of candidates. Caching files using `@functools.lru_cache` reduces overhead dramatically while keeping the API compliant by explicitly invalidating prompt caches on refinement.
**Action:** Use memory memoization for disk files in core pipelines, but ensure invalidation hooks are added on mutation endpoints.
