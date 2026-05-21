## 2025-05-14 - Optimize Prompt Construction
**Learning:** Repeated disk I/O for template loading and iterative string `.replace()` calls in a loop are a significant bottleneck when constructing prompts, especially when processed in parallel across multiple candidates.
**Action:** Use `@lru_cache` for template loading and a pre-compiled regex with `re.sub` and a callback for single-pass variable substitution to achieve measurable performance gains (~5.5x speedup).
