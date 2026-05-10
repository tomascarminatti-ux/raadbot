## 2024-05-05 - Optimized Prompt Construction
**Learning:** Repeated disk I/O and string replacements for prompt building is a bottleneck during parallel execution. Using caching and single-pass regex replacement significantly improves throughput.
**Action:** Always use lru_cache for template loading and prefer single-pass regex replacement when dealing with multiple placeholders in large text blocks.
