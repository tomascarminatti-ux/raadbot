## 2025-05-15 - Redundant Disk I/O in Prompt Building
**Learning:** The prompt builder was reading template files from disk for every GEM execution. In a parallel pipeline with many candidates, this creates significant I/O overhead and contention.
**Action:** Implement memoization using `functools.lru_cache` for template loading functions to ensure each file is only read once per process.
