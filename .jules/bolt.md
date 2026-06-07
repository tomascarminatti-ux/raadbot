## 2025-05-14 - Optimized build_prompt with caching and single-pass regex
**Learning:** build_prompt was previously doing disk I/O and multiple string replacements for every call. For multi-candidate pipelines, this overhead accumulates. Using lru_cache for templates and re.sub for variable replacement significantly reduces latency.
**Action:** Always cache static templates and use single-pass regex for multi-variable substitution in performance-critical paths.
