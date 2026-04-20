## 2025-05-22 - [Optimizing Prompt Generation with Caching and Regex]
**Learning:** Prompt building in agentic workflows is often a hidden bottleneck. Repeated disk I/O for templates and O(N) string replacements (where N is the number of variables) cause significant overhead. In this codebase, these factors combined to make `build_prompt` take ~0.13ms per call.
**Action:** Use `@lru_cache` for template loading and a single-pass `re.sub` with a lookup dictionary for variable substitution. This combination reduced execution time by ~73% to ~0.03ms per call.
