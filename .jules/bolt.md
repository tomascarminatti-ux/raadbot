## 2025-05-15 - [Prompt & Validation Optimization]
**Learning:** Sequential string replacements and repeated JSON schema compilation introduce significant overhead in agentic pipelines. Using single-pass regex for prompt injection and pre-compiling JSON validators can yield ~4x speedup in these logic-heavy paths.
**Action:** Always use `functools.lru_cache` for static template loading and `re.sub` with a mapping function for multi-variable injection. Pre-compile JSON schemas during class initialization.
