## 2025-05-24 - Optimized Prompt Construction with Caching and Single-Pass Substitution

**Learning:** Repeated disk I/O and iterative string replacements (`str.replace` in a loop) are significant bottlenecks in template-heavy applications, especially when processed in parallel. Using `lru_cache` for template loading and `re.sub` with a callback for single-pass replacement drastically reduces overhead.

**Action:** Always cache static template files and use single-pass regex substitution instead of multiple `str.replace` calls when injecting multiple variables into a large string.
