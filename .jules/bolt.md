## 2025-05-15 - Prompt Builder Optimization
**Learning:** Prompt construction was a bottleneck due to redundant disk I/O and multiple `str.replace` calls. Using `lru_cache` and a single-pass `re.sub` yielded a ~4x performance improvement.
**Action:** Always cache static templates and use regex for batch variable injection in template engines.
