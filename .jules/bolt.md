## 2025-05-15 - Optimized Prompt Construction
**Learning:** In LLM pipelines that process multiple items, redundant prompt construction (loading templates from disk and iterative string replacement) can become a significant micro-bottleneck. Using `lru_cache` for template loading and a single-pass `re.sub` for variable injection provides a measurable speedup.
**Action:** Always use caching for static templates and prefer regex-based single-pass substitution over multiple `str.replace` calls for complex string templates.
