# Bolt's Performance Journal

## 2025-05-24 - Efficient Template Substitution and I/O Caching
**Learning:** In a pipeline that processes multiple candidates in parallel, repeated disk I/O for prompt templates and iterative string replacements become a significant bottleneck. A single-pass `re.sub` with a callback is much more efficient than multiple `.replace()` calls, but we must ensure that the "master" template is injected *before* the single-pass substitution to resolve its internal variables.
**Action:** Use `lru_cache` for file-based templates and implement a two-stage build: 1. Inject static component templates (like Maestro) using `.replace()`. 2. Use a single-pass `re.sub` with a callback for dynamic variables.
