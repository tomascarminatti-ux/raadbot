## 2025-05-15 - [Prompt Building & Schema Loading Optimization]
**Learning:** Repetitive disk I/O for static resources (templates, schemas) and sequential string replacements are significant bottlenecks in high-frequency paths like prompt construction. Single-pass regex substitution with `re.sub` is much more efficient than chained `.replace()` calls.
**Action:** Use `lru_cache` for all static file loading and prefer `re.sub` with callbacks for multi-variable template injection.
