## 2025-05-15 - Optimizing Prompt Construction and State Persistence

**Learning:** Prompt construction using multiple `str.replace` calls is a significant bottleneck when dealing with many variables. Switching to a single `re.sub` pass with a callback function improved performance by ~6.1x. Additionally, redundant disk I/O for static assets (JSON schemas, prompt templates) can be easily eliminated using `functools.lru_cache` or global variables.

**Action:** Prefer single-pass regex substitution for template systems and always implement caching for static configuration/template files that are read frequently. Avoid redundant state writes by batching updates when possible.
