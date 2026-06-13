## 2026-06-13 - [Optimize prompt building with caching and single-pass injection]
**Learning:** In a template-heavy application like Raadbot, where prompts are frequently constructed from static markdown files, disk I/O and repetitive string replacements can become a significant overhead. Using `functools.lru_cache` for template loading and a single-pass `re.sub` for variable injection provides a measurable performance boost.
**Action:** Use tiered caching for templates and single-pass regex substitution for variable injection in future prompt-related optimizations.
