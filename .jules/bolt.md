## 2025-05-24 - Prompt Construction Optimization
**Learning:** Iterative `str.replace()` calls on long prompt templates with many variables cause $O(N \times M)$ overhead. Disk I/O for loading templates on every call adds significant latency, especially when processing many candidates in parallel.
**Action:** Use `@lru_cache` for template loading and a single-pass `re.sub()` with a callback for variable replacement to achieve $O(N)$ efficiency and avoid redundant I/O.
