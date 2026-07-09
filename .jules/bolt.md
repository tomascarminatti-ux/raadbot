## 2025-05-22 - [Optimizing Prompt Construction]
**Learning:** Eliminating redundant disk I/O and iterative string replacements in prompt construction provides order-of-magnitude speedups. Using `lru_cache` for templates and a single-pass `re.sub` with a callback is much more efficient than multiple `str.replace` calls.
**Action:** Use cached template loaders and single-pass regex replacement for any high-frequency string templating tasks.
