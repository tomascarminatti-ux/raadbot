## 2026-04-20 - [Optimizing Prompt Construction and Disk I/O]
**Learning:** For LLM agents with sequential or parallel pipelines, redundant disk I/O (loading prompts, schemas) and string processing in retry loops are common bottlenecks. Using a single-pass `re.sub` with a callback is significantly faster (~4x) than multiple `.replace()` calls for template resolution.
**Action:** Always move static operations like prompt building outside of retry loops and use `@lru_cache` for frequent file reads.
