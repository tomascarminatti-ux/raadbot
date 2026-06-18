## 2026-06-18 - [Optimized Prompt Builder]
**Learning:** Disk I/O in hot paths (like repeated prompt template loading) is a major anti-pattern; caching static templates in memory using lru_cache and using single-pass regex substitution for variable injection provides significant speedups.
**Action:** Use lru_cache for static file loading and re.sub for high-frequency string template injection.
