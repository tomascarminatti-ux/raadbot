## 2025-05-22 - [Optimizing Prompt Builder]
**Learning:** In LLM pipelines, prompt construction can become a bottleneck if templates are re-read from disk on every call. Additionally, multiple `.replace()` calls on large strings create many intermediate string copies.
**Action:** Use `functools.lru_cache` for template loading and a single `re.sub` pass with a regex callback for variable injection to minimize memory pressure and CPU overhead.
