## 2025-05-14 - Optimized Prompt Construction
**Learning:** Repeated disk I/O and iterative string replacement using `.replace()` in a loop is a significant bottleneck for prompt building, especially as the number of variables grows. Using `@lru_cache` for templates and a single-pass `re.sub()` with a pre-compiled pattern provides a substantial performance boost (~5x in this case).
**Action:** Always prefer single-pass regex substitution for templating systems and cache file-based templates to avoid redundant I/O.
