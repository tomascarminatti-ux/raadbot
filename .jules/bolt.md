## 2025-05-24 - Optimized Prompt Construction with Caching and Regex

**Learning:** Repeated disk I/O for prompt templates and iterative string replacement using `.replace()` in a loop is a significant bottleneck when building complex prompts. Implementing `@lru_cache` for template loading and switching to a single-pass `re.sub()` with a callback significantly improves performance (~30x speedup). Crucially, the `{{PROMPT_MAESTRO}}` placeholder must be replaced *before* the regex pass to ensure any placeholders within the maestro template itself are subsequently resolved by the regex substitution.

**Action:** Always use cached loaders for templates and favor single-pass regex substitution for multi-variable template injection. Ensure hierarchical template injections (like maestro) are performed in the correct order to allow nested variable resolution.
