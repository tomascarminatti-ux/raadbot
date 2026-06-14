## 2025-05-22 - [Optimizing Template Building]
**Learning:** Disk I/O in hot paths (like repeated prompt template loading) is a major anti-pattern; caching static templates in memory using lru_cache provides significant speedups. Additionally, for high-frequency string template injection, a single-pass regex substitution with a callback function is significantly more efficient than multiple sequential str.replace() calls.
**Action:** Always use caching for static assets and prefer single-pass regex for complex string templating in performance-critical sections.
