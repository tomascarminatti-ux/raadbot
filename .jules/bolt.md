## 2025-05-14 - Optimized Prompt Building and Schema Loading
**Learning:** In a prompt-heavy application, redundant disk I/O for templates and schema files can become a bottleneck when processing multiple candidates. Additionally, iterative string replacement for large prompts is significantly slower than single-pass regex substitution.
**Action:** Always implement caching for static resources like JSON schemas and markdown templates. Use `re.sub` with a callback for bulk variable replacement in strings to achieve O(L) instead of O(V*L) complexity.
