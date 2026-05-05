## 2026-05-05 - Optimize Prompt Construction with Caching and Single-pass Regex

**Learning:** Repeatedly loading prompt templates from disk and performing multiple `str.replace` operations for each variable creates unnecessary overhead, especially in parallel execution scenarios (like processing multiple candidates). Pre-compiling regex and using `lru_cache` significantly reduces latency.

**Action:** Always cache template files and use `re.sub` with a callback for single-pass variable substitution in template-heavy modules.
