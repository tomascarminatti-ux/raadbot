## 2025-05-14 - Redundant I/O and Disk Access
**Learning:** Frequent disk writes (state persistence) and repeated reads of static template files (prompts) are significant performance bottlenecks in agent pipelines.
**Action:** Use `@lru_cache` for static file loading and ensure state persistence only occurs at logical completion boundaries rather than on every minor update.
