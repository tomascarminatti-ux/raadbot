## 2026-07-04 - Optimized prompt construction and contract validation
**Learning:** Eliminating redundant disk I/O and iterative string replacements in prompt construction and schema validation provides order-of-magnitude speedups in LLM-intensive pipelines.
**Action:** Always use `lru_cache` for loading static templates/schemas and prefer single-pass `re.sub` with a callback for template variable injection over multiple `str.replace` calls.
