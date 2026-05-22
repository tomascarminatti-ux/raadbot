## 2024-05-11 - Optimized Prompt Building
**Learning:** Repeated disk I/O for prompt templates and iterative string replacement is a bottleneck when building many prompts in parallel (e.g., in a pipeline).
**Action:** Implement LRU caching for template loading and use single-pass regex substitution for variable injection.
