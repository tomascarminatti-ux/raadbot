## 2025-05-24 - Optimized Prompt Building with Caching and Regex

**Learning:** Repeated disk I/O for prompt templates and iterative string replacement (multiple `.replace()` calls) is a significant bottleneck in parallel execution environments like `GEM6Orchestrator`. A single-pass regex substitution with a callback is more efficient and maintains correctness for complex templates.

**Action:** Use `@lru_cache` for template loading functions and `re.sub` for single-pass variable injection. Ensure `{{PROMPT_MAESTRO}}` is injected *before* other variables so that any placeholders within the maestro template are also resolved.
