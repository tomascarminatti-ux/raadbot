## 2025-05-14 - Optimized prompt construction and contract validation
**Learning:** Redundant disk I/O and iterative string replacements in prompt templates are significant bottlenecks in high-frequency LLM pipelines. Implementing `lru_cache` for templates/schemas and single-pass regex substitution for variable injection provides an order-of-magnitude speedup.
**Action:** Always use caching for static assets like prompts and schemas. Use regex callbacks for multi-variable injection instead of iterative `str.replace`.
