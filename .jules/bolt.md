## 2025-05-15 - Single-pass Prompt Construction & Schema Caching
**Learning:** In LLM-intensive applications, prompt construction and schema validation can become silent bottlenecks. Replacing iterative `str.replace` calls (which recreate strings multiple times) with a single-pass `re.sub` callback and using `lru_cache` to eliminate redundant disk I/O for static templates/schemas yields order-of-magnitude (up to 12x) speedups.
**Action:** Always prioritize single-pass variable injection and I/O caching for core orchestration utilities.
