
## 2026-06-17 - Caching and Regex substitution in Prompt Builder
**Learning:** Repeated disk I/O for static templates and multiple string replacements are significant bottlenecks in high-frequency prompt generation. Caching templates with lru_cache and using single-pass regex substitution significantly improves performance.
**Action:** Use lru_cache for static file loading and re.sub with callback for template injection.
