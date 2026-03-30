## 2025-05-15 - [Prompt Template Caching]
**Learning:** Reading static prompt files from disk on every `build_prompt` call introduced unnecessary I/O overhead. Since these templates (and the Maestro prompt) are immutable during execution, caching them significantly improves performance.
**Action:** Use `functools.lru_cache` for file-loading functions and pre-compile regexes used in hot loops to minimize string processing and I/O costs.
