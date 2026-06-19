## 2025-05-14 - [Optimize prompt builder with template caching and single-pass substitution]
**Learning:** Disk I/O in the hot path of building prompts is a significant bottleneck, especially when templates are loaded repeatedly. Also, sequential `str.replace()` calls are less efficient than a single-pass regex substitution with a callback.
**Action:** Use `lru_cache` for static template loading and `re.sub()` with a replacement function for multiple placeholders.
