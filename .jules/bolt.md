## 2026-06-20 - Prompt Template Caching and Single-pass Regex Injection
**Learning:** Disk I/O for reading prompt templates on every call is a significant bottleneck. Using multiple `str.replace()` calls is inefficient compared to a single-pass regex substitution with a callback, especially when many variables are involved.
**Action:** Always use `lru_cache` for static file loads in hot paths. For bulk string replacements, prefer `re.sub` with a mapping or callback.
