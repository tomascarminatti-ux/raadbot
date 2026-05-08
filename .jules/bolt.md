## 2024-05-05 - Optimized Prompt Construction
**Learning:** Repeated disk I/O for loading templates and multiple `str.replace` calls for variable substitution create a significant bottleneck when processing many candidates in parallel.
**Action:** Implement `lru_cache` for template loading and use a single-pass `re.sub` for variable replacement to achieve O(M+N) complexity instead of O(M*N).
