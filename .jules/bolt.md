## 2025-05-15 - Optimized prompt construction and contract validation
**Learning:** For LLM-intensive applications, prompt construction and contract validation can become a significant CPU/IO bottleneck. Multiple `str.replace` calls on large templates are inefficient, and repeated disk reads for static templates/schemas add unnecessary latency.
**Action:** Use `functools.lru_cache` for file loading (prompts, schemas) and `re.sub` with a callback for single-pass template variable injection. This achieved ~9-17x speedup in core utility paths.
