## 2024-05-11 - Optimized prompt template loading and variable injection
**Learning:** Repeated disk I/O for static templates and iterative `str.replace` calls for variable injection are significant bottlenecks in prompt construction.
**Action:** Use `functools.lru_cache` for template loading and a single-pass `re.sub` with a dictionary-based replacer function for efficient multi-variable injection.
