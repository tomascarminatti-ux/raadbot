## 2025-05-14 - Optimized Prompt Construction
**Learning:** Repeated disk I/O and multiple `.replace()` calls in a loop are a significant bottleneck for prompt construction, especially when processing multiple candidates in parallel.
**Action:** Use `@lru_cache` for template loading and a single-pass `re.sub()` with a replacer function for efficient variable injection.
