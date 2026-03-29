## 2025-05-14 - Eliminating redundant I/O in Prompt/Schema loading
**Learning:** Disk I/O for static assets like prompt templates and JSON schemas, combined with repetitive regex compilation, created a measurable bottleneck. Using `@lru_cache` on file loading functions and pre-compiling regexes at the module level reduced `build_prompt` overhead by ~55%.
**Action:** Always pre-compile regexes used in loops and cache static file reads (prompts, schemas, config) using `functools.lru_cache` to minimize I/O and CPU overhead.
