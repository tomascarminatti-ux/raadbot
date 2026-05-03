## 2025-05-15 - Optimize Prompt Building with Single-Pass Regex
**Learning:** Using `re.sub` with a callback for variable substitution in prompt templates is significantly more efficient than nested loops or multiple `.replace()` calls. In this codebase, it reduced `build_prompt` latency by ~4.8x. Combined with `lru_cache` for template loading, it avoids redundant disk I/O.
**Action:** Always prefer `re.sub` with a dictionary-based callback for template variable injection. Use `functools.lru_cache` for static file loading.
