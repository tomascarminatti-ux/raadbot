## 2026-07-02 - Optimized Prompt Construction
**Learning:** In LLM-heavy applications, building prompts by iteratively calling `.replace()` on large strings is a hidden bottleneck. Each call creates a new string copy. Switching to a single-pass `re.sub()` with a callback function for variable injection, combined with `lru_cache` for template loading, significantly reduces overhead.
**Action:** Always prefer single-pass regex substitution for template systems and use `@lru_cache` for static file assets like prompt templates.
