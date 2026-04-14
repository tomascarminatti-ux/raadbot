## 2025-05-15 - [Prompt Builder Optimization]
**Learning:** In a template-heavy application, repeated disk I/O and multiple `str.replace` calls can be a significant bottleneck. Using `functools.lru_cache` for template loading and `re.sub` with a callback for single-pass replacement provides a measurable performance boost. Also, Python's `lru_cache` uses `maxsize`, not `max_size`.
**Action:** Always consider caching for static or semi-static assets like templates and use regex for batch string replacements.
