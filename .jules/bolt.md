## 2025-05-14 - Optimized Prompt Building with Tiered Caching

**Learning:** Loading prompt templates from disk and performing multiple sequential `.replace()` calls for every prompt generation creates a measurable bottleneck (~0.77ms per call). This is especially impactful in orchestrators like GEM6 that call multiple agents.

**Action:** Implement tiered `lru_cache`: one for raw file reads (`load_prompt`) and another for combined templates (`_get_template_with_maestro`). Use `re.sub` with a callback for single-pass variable injection to avoid redundant string passes.
