## 2025-02-28 - Optimize Prompt Building with Caching and Single-Pass Regex
**Learning:** For template systems with multiple variables, a single-pass `re.sub` with a callback is significantly more efficient than a loop of `str.replace` calls. Combined with `lru_cache` for file I/O, prompt construction time was reduced by ~90% (from ~157µs to ~16µs).
**Action:** Use `re.sub` for multi-variable substitution and `lru_cache` for template loading in high-frequency LLM pipelines.
