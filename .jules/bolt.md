## 2025-05-22 - Optimized Prompt Construction
**Learning:** Prompt template injection was performing redundant disk I/O and multiple full-string scans for variable substitution. Caching templates and using a single-pass regex `sub` with a callback significantly reduces latency, especially as templates or variable counts grow.
**Action:** Use `@lru_cache` for static file loading and `re.sub` with a callback for bulk string replacements to minimize O(n*m) complexity to O(n).
