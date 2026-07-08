# Bolt's Performance Journal

## 2025-07-08 - [Optimizing Prompt Construction and Contract Validation]
**Learning:** Redundant disk I/O for static assets (templates, schemas) and iterative string replacements in template engines are significant bottlenecks in high-frequency loops (like processing hundreds of candidates). `functools.lru_cache` and single-pass `re.sub` provide order-of-magnitude speedups.
**Action:** Always use caching for static template/schema loading and prefer single-pass regex replacement over iterative `str.replace` for template engines.
