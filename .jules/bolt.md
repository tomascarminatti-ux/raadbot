# Bolt's Performance Journal

## 2024-05-11 - Optimized Prompt Builder with Caching and Regex
**Learning:** Sequential `str.replace` calls on large templates with many variables cause multiple full string traversals (O(N*M)). Using `re.sub` with a callback function allows for a single-pass replacement (O(N)). Additionally, repeatedly reading template files from disk is a major bottleneck in high-frequency operations like parallel LLM orchestration.
**Action:** Use `re.sub` with a callback for efficient multi-variable replacement and apply `@lru_cache` to file-loading functions to minimize disk I/O.
